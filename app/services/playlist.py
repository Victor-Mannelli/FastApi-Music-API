from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import subqueryload, selectinload
from sqlalchemy.future import select
from app.services import music as music_service
from app.db.models import Playlist as playlist_model
from app.db.models import Music as music_model
from app.schemas import playlist as playlist_schemas


async def create_playlist(
    db: AsyncSession, playlist: playlist_schemas.PlaylistBase, user_id: int
):
    db_playlist = playlist_model(
        private=playlist.private,
        name=playlist.name,
        owner_id=user_id,
    )
    db.add(db_playlist)
    try:
        await db.commit()
        await db.refresh(db_playlist)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="playlist already exists",
        )
    return db_playlist


async def add_music_to_playlist(
    db: AsyncSession,
    requester_id: int,
    playlist_id: int,
    music_id: int,
):
    # Use selectinload or joinedload to eagerly load musics
    statement = (
        select(playlist_model)
        .options(selectinload(playlist_model.musics))  # Eagerly load musics
        .filter(playlist_model.id == playlist_id)
    )
    result = await db.execute(statement)
    db_playlist = result.scalar_one_or_none()
    if not db_playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found"
        )

    if db_playlist.owner_id != requester_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only add music to your own playlists",
        )

    # Ensure music is fetched asynchronously
    db_music = await music_service.get_music_by_id(db=db, music_id=music_id)
    if not db_music:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Music not found"
        )
    if db_music in db_playlist.musics:
        raise HTTPException(
            status_code=400, detail="Music already exists in the playlist"
        )

    db_playlist.musics.append(db_music)
    try:
        # Ensure commit is done asynchronously
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Error adding music to playlist")

    return db_music


async def get_playlist_by_id(db: AsyncSession, playlist_id: int):
    try:
        return await db.get(playlist_model, playlist_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found",
        )


async def get_user_playlists(db: AsyncSession, user_id: int, requester_id: int = None):
    if requester_id is not None and requester_id == user_id:
        statement = select(playlist_model).filter(
            (playlist_model.owner_id == user_id)
            & ((playlist_model.private == True) | (playlist_model.private == False))
        )
    else:
        statement = select(playlist_model).filter(
            (playlist_model.owner_id == user_id) & (playlist_model.private == False)
        )

    result = await db.execute(statement)
    return result.scalars().all()


async def get_playlist_musics(
    db: AsyncSession, playlist_id: int, requester_id: int = None
):
    statement = (
        select(playlist_model)
        .filter(playlist_model.id == playlist_id)
        .options(subqueryload(playlist_model.musics))
    )
    result = await db.execute(statement)
    db_playlist = result.scalar_one_or_none()
    if not db_playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found",
        )

    if db_playlist.private == True:
        if requester_id is not None and requester_id == db_playlist.owner_id:
            return db_playlist
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )
    else:
        return db_playlist


async def remove_music_from_playlist(db: AsyncSession, music_id: int, playlist_id: int):
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
    db: AsyncSession, playlist_id: int, playlist: playlist_schemas.PlaylistUpdate
):
    db_playlist = await get_playlist_by_id(db=db, playlist_id=playlist_id)
    if playlist.name:
        db_playlist.name = playlist.name
    if playlist.private is not None:
        db_playlist.private = playlist.private

    await db.commit()
    await db.refresh(db_playlist)
    return db_playlist


async def delete_playlist(db: AsyncSession, playlist_id: int):
    db_playlist = await get_playlist_by_id(db=db, playlist_id=playlist_id)
    await db.delete(db_playlist)
    await db.commit()
    return db_playlist
