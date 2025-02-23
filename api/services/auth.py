import jwt
from api.config.setup import JWT_SECRET, ALGORITHM
from ..db.models import User as user_model
from datetime import datetime, timedelta
from passlib.context import CryptContext
from api.db.core import get_db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# * get current user based on token
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
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
    user = db.query(user_model).filter(user_model.id == user_id).first()
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
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(user_model).filter(user_model.email == email).first()
    if not user or not verify_password(password, user.password):
        return None
    return user


# * creates and returns a JWT token
# * dict data is the user info
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
