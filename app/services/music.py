from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.db.models import Music as music_model
from app.schemas import music as music_schemas


async def add_music(db: AsyncSession, music: music_schemas.MusicBase, user_id: int):
    db_music = music_model(
        title=music.title,
        artist=music.artist,
        link=music.link,
        added_by=user_id,
    )
    db.add(db_music)
    try:
        await db.commit()
        await db.refresh(db_music)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Music already exists",
        )
    return db_music


async def get_musics(db: AsyncSession, skip: int = 0, limit: int = 10):
    statement = select(music_model).offset(skip).limit(limit)
    result = await db.execute(statement)
    return result.scalars().all()


async def get_user_added_musics(
    db: AsyncSession, user_id: int, skip: int = 0, limit: int = 10
):
    statement = (
        select(music_model)
        .where(music_model.added_by == user_id)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(statement)
    return result.scalars().all()


async def get_music_by_id(db: AsyncSession, music_id: int):
    try:
        return await db.get(music_model, music_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Music not found",
        )


async def update_music(
    db: AsyncSession, music_id: int, music: music_schemas.MusicUpdate
):
    db_music = await get_music_by_id(db=db, music_id=music_id)
    if music.title:
        db_music.title = music.title
    if music.artist:
        db_music.artist = music.artist
    if music.link:
        db_music.link = music.link
    await db.commit()
    await db.refresh(db_music)
    return db_music


async def remove_music(db: AsyncSession, music_id: int):
    db_music = await get_music_by_id(db=db, music_id=music_id)
    await db.delete(db_music)
    await db.commit()
    return db_music
