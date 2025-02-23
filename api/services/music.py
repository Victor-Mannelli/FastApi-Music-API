from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..db.models import Music as musicModel
from ..schemas import music as musicSchemas


def add_music(db: Session, music: musicSchemas.MusicBase, user_id: int):
    db_music = musicModel(
        title=music.title,
        artist=music.artist,
        link=music.link,
        added_by=user_id,
    )
    db.add(db_music)
    try:
        db.commit()
        db.refresh(db_music)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Music already exists",
        )
    return db_music


def get_musics(db: Session, skip: int = 0, limit: int = 10):
    return db.query(musicModel).offset(skip).limit(limit).all()


def get_user_added_musics(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(musicModel)
        .filter(musicModel.added_by == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_music_by_id(db: Session, music_id: int):
    return db.query(musicModel).filter(musicModel.id == music_id).first()


def update_music(db: Session, music_id: int, music: musicSchemas.MusicUpdate):
    db_music = db.query(musicModel).filter(musicModel.id == music_id).first()
    if not db_music:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Music not found"
        )
    if music.title:
        db_music.title = music.title
    if music.artist:
        db_music.artist = music.artist
    if music.link:
        db_music.link = music.link
    db.commit()
    db.refresh(db_music)
    return db_music


def remove_music(db: Session, music_id: int):
    db_music = db.query(musicModel).filter(musicModel.id == music_id).first()
    if not db_music:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Music not found"
        )
    db.delete(db_music)
    db.commit()
    return db_music
