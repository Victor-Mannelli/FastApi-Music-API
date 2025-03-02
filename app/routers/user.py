from fastapi import APIRouter, Depends, HTTPException, status
from app.config.setup import ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.functions import checkUserAuthenticity
from app.services import user as user_services
from app.services import auth as auth_services
from app.schemas import user as user_schema
from app.db.core import get_async_db
from sqlalchemy.orm import Session
from datetime import timedelta

router = APIRouter(prefix="/users")


# * Get user info and checks if token is valid
@router.get("/me", response_model=user_schema.UserOut)
async def get_current_user_info(
    current_user: user_schema.UserBase = Depends(auth_services.get_current_user),
):
    return current_user


# * Login
@router.post("/login", response_model=user_schema.LoginOut)
async def login(user_data: user_schema.UserLogin, db: Session = Depends(get_async_db)):
    user = await auth_services.authenticate_user(
        db, user_data.email, user_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect email or password"
        )

    access_token = auth_services.create_access_token(
        data={"sub": user.id, "username": user.username, "email": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


# * Registration
@router.post(
    "", response_model=user_schema.UserOut, status_code=status.HTTP_201_CREATED
)
async def create_user(
    user: user_schema.UserCreate, db: Session = Depends(get_async_db)
):
    return await user_services.create_user(db=db, user=user)


# * Get a user by ID
@router.get("/{user_id}", response_model=user_schema.UserOut)
async def get_user(user_id: int, db: Session = Depends(get_async_db)):
    db_user = await user_services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


# * Get all users
@router.get("", response_model=list[user_schema.UserOut])
async def get_users(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_async_db)
):
    users = await user_services.get_users(db=db, skip=skip, limit=limit)
    return users


# * Update user by ID
@router.put("/{user_id}", response_model=user_schema.UserOut)
async def update_user(
    user_id: int,
    updated_user: user_schema.UserUpdate,
    db: Session = Depends(get_async_db),
    current_user: user_schema.UserOut = Depends(auth_services.get_current_user),
):
    checkUserAuthenticity(user_id, current_user_id=current_user.id)
    return await user_services.update_user(
        db=db, user_id=user_id, updated_user=updated_user
    )


# * Delete user by ID
@router.delete("/{user_id}", response_model=user_schema.UserOut)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_async_db),
    current_user: user_schema.UserOut = Depends(auth_services.get_current_user),
):
    checkUserAuthenticity(user_id, current_user_id=current_user.id)
    return await user_services.delete_user(db=db, user_id=user_id)
