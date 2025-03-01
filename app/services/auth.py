import jwt
from app.config.setup import JWT_SECRET, ALGORITHM
from app.db.models import User as user_model
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.future import select
from app.db.core import get_async_db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# * get current user based on token
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_db)
):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_id = payload.get("sub")  # * 'sub' is where the user_id is stored
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    # * Get the user from the database based on the user_id
    result = await db.execute(select(user_model).filter(user_model.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


# * hash the password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# * check if hashed password matches the plain password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# * checks if user exists and password is correct
async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(select(user_model).filter(user_model.email == email))
    user = result.scalars().first()
    if not user or not verify_password(password, user.password):
        return None
    return user


# * creates and returns a JWT token
# * dict data is user info that's goona be JWT payload data
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)


# * checks if token is valid and returns jwt payload
def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload  # * This will contain the user info
    except jwt.ExpiredSignatureError:
        return None  # * Token expired
    except jwt.InvalidTokenError:
        return None  # * Invalid token
