from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.future import select
from fastapi import HTTPException, status
from ..services import auth as auth_services
from ..db.models import User as user_model
from ..schemas import user as user_schemas


async def create_user(db: AsyncSession, user: user_schemas.UserCreate):
    hashed_password = auth_services.get_password_hash(
        user.password
    )  # Hash the password
    db_user = user_model(
        username=user.username,
        email=user.email,
        password=hashed_password,  # Store the hashed password
    )
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        )
    return db_user


async def get_user(db: AsyncSession, user_id: int):
    try:
        return await db.get(user_model, user_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    statement = select(user_model).offset(skip).limit(limit)
    result = await db.execute(statement)
    return result.scalars().all()


# ! This is not updating user password
async def update_user(
    db: AsyncSession, user_id: int, updated_user: user_schemas.UserUpdate
):
    db_user = await get_user(db=db, user_id=user_id)
    if updated_user.username:
        db_user.username = updated_user.username
    if updated_user.email:
        db_user.email = updated_user.email
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int):
    db_user = await get_user(db=db, user_id=user_id)

    await db.delete(db_user)
    await db.commit()
    return db_user
