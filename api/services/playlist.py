from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, subqueryload
from ..db.models import Playlist as playlist_model
from ..db.models import Music as music_model
from ..schemas import playlist as playlist_schemas


def create_playlist(db: Session, playlist: playlist_schemas.PlaylistBase, user_id: int):
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


def add_music_to_playlist(db: Session, music_id: int, playlist_id: int):
    db_playlist = (
        db.query(playlist_model).filter(playlist_model.id == playlist_id).first()
    )
    if not db_playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found"
        )
    db_music = db.query(music_model).filter(music_model.id == music_id).first()
    if db_music in db_playlist.musics:
        raise HTTPException(
            status_code=400, detail="Music already exists in the playlist"
        )
    db_playlist.musics.append(db_music)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error adding music to playlist")

    return db_playlist


def get_playlist_by_id(db: Session, playlist_id: int):
    return db.query(playlist_model).filter(playlist_model.id == playlist_id).first()


def get_user_playlists(db: Session, user_id: int):
    return db.query(playlist_model).filter(playlist_model.owner_id == user_id).all()


def get_playlist_musics(db: Session, playlist_id: int):
    return (
        db.query(playlist_model)
        .filter(playlist_model.id == playlist_id)
        .options(subqueryload(playlist_model.musics))
        .first()
    )


def remove_music_from_playlist(db: Session, music_id: int, playlist_id: int):
    db_playlist = (
        db.query(playlist_model).filter(playlist_model.id == playlist_id).first()
    )
    if not db_playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found"
        )
    db_music = db.query(music_model).filter(music_model.id == music_id).first()
    if db_music not in db_playlist.musics:
        raise HTTPException(
            status_code=400, detail="Music does not exist in the playlist"
        )
    db_playlist.musics.remove(db_music)
    db.commit()
    return db_playlist


def update_playlist(
    db: Session, playlist_id: int, playlist: playlist_schemas.PlaylistUpdate
):
    db_playlist = (
        db.query(playlist_model).filter(playlist_model.id == playlist_id).first()
    )
    if not db_playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found"
        )
    if playlist.name:
        db_playlist.name = playlist.name
    db.commit()
    db.refresh(db_playlist)
    return db_playlist


def delete_playlist(db: Session, playlist_id: int):
    db_playlist = (
        db.query(playlist_model).filter(playlist_model.id == playlist_id).first()
    )
    if not db_playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found"
        )
    db.delete(db_playlist)
    db.commit()
    return db_playlist
