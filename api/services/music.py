from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..db.models import Music as music_model
from ..schemas import music as music_schemas


def add_music(db: Session, music: music_schemas.MusicBase, user_id: int):
    db_music = music_model(
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
    return db.query(music_model).offset(skip).limit(limit).all()


def get_user_added_musics(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(music_model)
        .filter(music_model.added_by == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_music_by_id(db: Session, music_id: int):
    return db.query(music_model).filter(music_model.id == music_id).first()


def update_music(db: Session, music_id: int, music: music_schemas.MusicUpdate):
    db_music = db.query(music_model).filter(music_model.id == music_id).first()
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
    db_music = db.query(music_model).filter(music_model.id == music_id).first()
    if not db_music:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Music not found"
        )
    db.delete(db_music)
    db.commit()
    return db_music
