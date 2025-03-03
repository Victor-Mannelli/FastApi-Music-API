import jwt
from app.config.setup import JWT_SECRET, ALGORITHM
from app.db.models import User as user_model
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.future import select
from app.db.core import get_async_db
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Custom dependency function to make the token optional
async def get_optional_current_user(
    request: Request,  # Manually extract the token from the header
    db: AsyncSession = Depends(get_async_db),
):
    token = request.headers.get("Authorization")  # Get token manually
    if token and token.startswith("Bearer "):
        token = token.split("Bearer ")[1]  # Extract only the token part
        return await get_current_user(db=db, token=token, optional=True)

    return None


# * get current user based on token
async def get_current_user(
    db: AsyncSession = Depends(get_async_db),
    token: str = Depends(oauth2_scheme),
    optional: bool = False,
):
    if optional and not token:
        return None

    payload = verify_token(token)

    user_id = payload.get("sub")  # * 'sub' is where the user_id is stored
    # * Get the user from the database based on the user_id
    user = await db.get(user_model, user_id)
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
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
