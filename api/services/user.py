from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..db.models import User as userModel
from ..schemas import user as userSchemas

print(f"DEBUG: Imported User: {userModel}")

def create_user(db: Session, user: userSchemas.UserCreate):
    db_user = userModel(
        username=user.username,
        email=user.email,
        password=user.password  # We will hash the password later in the authentication part
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(userModel).filter(userModel.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(userModel).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user: userSchemas.UserUpdate):
    db_user = db.query(userModel).filter(userModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.username:
        db_user.username = user.username
    if user.email:
        db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(userModel).filter(userModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user