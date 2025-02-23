from fastapi import APIRouter, Depends, HTTPException, status
from api.config.setup import ACCESS_TOKEN_EXPIRE_MINUTES
from sqlalchemy.orm import Session
from ..services import user as userServices
from ..services import auth as authServices
from ..schemas import user as user_schema
from datetime import timedelta
from ..db.core import get_db

router = APIRouter(prefix="/users")


# * Get user info and checks if token is valid
@router.get("/me")
def get_current_user_info(
    current_user: user_schema.UserBase = Depends(authServices.get_current_user),
):
    return {"user": current_user}


# * Login
@router.post("/login", response_model=user_schema.LoginOut)
def login(user_data: user_schema.UserLogin, db: Session = Depends(get_db)):
    user = authServices.authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect email or password"
        )

    access_token = authServices.create_access_token(
        data={"sub": user.id, "username": user.username, "email": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


# * Registration
@router.post("", response_model=user_schema.UserOut)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    return userServices.create_user(db=db, user=user)


# * Get a user by ID
@router.get("/{user_id}", response_model=user_schema.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = userServices.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


# * Get all users
@router.get("", response_model=list[user_schema.UserOut])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = userServices.get_users(db=db, skip=skip, limit=limit)
    return users


# * Update user by ID
@router.put("/{user_id}", response_model=user_schema.UserOut)
def update_user(
    user_id: int,
    user: user_schema.UserUpdate,
    db: Session = Depends(get_db),
    current_user: user_schema.UserOut = Depends(authServices.get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this user",
        )
    return userServices.update_user(db=db, user_id=user_id, user=user)


# Delete user by ID
@router.delete("/{user_id}", response_model=user_schema.UserOut)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.UserOut = Depends(authServices.get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this user",
        )
    return userServices.delete_user(db=db, user_id=user_id)
