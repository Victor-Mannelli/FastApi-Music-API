from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, subqueryload
from sqlalchemy.future import select
from app.services import music as music_service
from app.db.models import Playlist as playlist_model
from app.schemas import playlist as playlist_schemas
from app.db.models import Music as music_model


async def create_playlist(
    db: Session, playlist: playlist_schemas.PlaylistBase, user_id: int
):
    db_playlist = playlist_model(name=playlist.name, owner_id=user_id)
    db.add(db_playlist)
    try:
        db.commit()
        db.refresh(db_playlist)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="playlist already exists",
        )
    return db_playlist


async def add_music_to_playlist(db: Session, music_id: int, playlist_id: int):
    statement = select(playlist_model).filter(playlist_model.id == playlist_id)
    db_playlist = await db.execute(statement).scalar_one_or_none()
    if not db_playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found"
        )
    db_music = await music_service.get_music_by_id(music_id)
    if db_music in db_playlist.musics:
        raise HTTPException(
            status_code=400, detail="Music already exists in the playlist"
        )
    db_playlist.musics.append(db_music)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Error adding music to playlist")

    return db_playlist


async def get_playlist_by_id(db: Session, playlist_id: int):
    try:
        return await db.get(playlist_model, playlist_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found",
        )


async def get_playlist_musics(db: Session, playlist_id: int):
    return (
        db.query(playlist_model)
        .filter(playlist_model.id == playlist_id)
        .options(subqueryload(playlist_model.musics))
        .first()
    )


async def remove_music_from_playlist(db: Session, music_id: int, playlist_id: int):
    db_playlist = await get_playlist_by_id(db=db, playlist_id=playlist_id)
    db_music = await db.get(music_model, music_id)
    if db_music not in db_playlist.musics:
        raise HTTPException(
            status_code=400, detail="Music does not exist in the playlist"
        )

    db_playlist.musics.remove(db_music)
    await db.commit()
    return db_playlist


async def update_playlist(
    db: Session, playlist_id: int, playlist: playlist_schemas.PlaylistUpdate
):
    db_playlist = await get_playlist_by_id(db=db, playlist_id=playlist_id)
    if playlist.name:
        db_playlist.name = playlist.name
    await db.commit()
    await db.refresh(db_playlist)
    return db_playlist


async def delete_playlist(db: Session, playlist_id: int):
    db_playlist = await get_playlist_by_id(db=db, playlist_id=playlist_id)
    await db.delete(db_playlist)
    await db.commit()
    return db_playlist
