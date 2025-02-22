from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from api.config.setup import ACCESS_TOKEN_EXPIRE_MINUTES
from ..services import user as userServices
from ..services import auth as authServices
from ..schemas import user as userSchema
from datetime import timedelta
from ..db.core import get_db

router = APIRouter(prefix="/users")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = authServices.verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return payload


@router.get("/me")
def get_current_user_info(
    current_user: userSchema.UserBase = Depends(get_current_user),
):
    return {"user": current_user}


@router.post("/login")
def login(user_data: userSchema.UserLogin, db: Session = Depends(get_db)):
    user = authServices.authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = authServices.create_access_token(
        data={"sub": user.id, "username": user.username, "email": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("", response_model=userSchema.UserOut)
def create_user(user: userSchema.UserCreate, db: Session = Depends(get_db)):
    return userServices.create_user(db=db, user=user)


# Get a user by ID
@router.get("/{user_id}", response_model=userSchema.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = userServices.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Get all users
@router.get("", response_model=list[userSchema.UserOut])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = userServices.get_users(db=db, skip=skip, limit=limit)
    return users


# Update user by ID
@router.put("/{user_id}", response_model=userSchema.UserOut)
def update_user(
    user_id: int, user: userSchema.UserUpdate, db: Session = Depends(get_db)
):
    return userServices.update_user(db=db, user_id=user_id, user=user)


# Delete user by ID
@router.delete("/{user_id}", response_model=userSchema.UserOut)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return userServices.delete_user(db=db, user_id=user_id)
