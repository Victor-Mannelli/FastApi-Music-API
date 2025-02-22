from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.core import get_db
from ..schemas import user as userSchema 
from ..services import user as userServices

router = APIRouter(
  prefix="/users"
)

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
def update_user(user_id: int, user: userSchema.UserUpdate, db: Session = Depends(get_db)):
    return userServices.update_user(db=db, user_id=user_id, user=user)


# Delete user by ID
@router.delete("/{user_id}", response_model=userSchema.UserOut)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return userServices.delete_user(db=db, user_id=user_id)