from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..services import music as music_services
from ..services import user as user_services
from ..services import auth as auth_services
from ..schemas import music as music_schema
from ..schemas import user as user_schema
from ..db.core import get_db

router = APIRouter(prefix="/music")


# * Add music to the db
@router.post("", response_model=music_schema.MusicOut)
def add_music(
    music: music_schema.MusicBase,
    db: Session = Depends(get_db),
    current_user: user_schema.UserJwtPayload = Depends(auth_services.get_current_user),
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You need to be logged in to add music",
        )
    return music_services.add_music(db=db, music=music, user_id=current_user["sub"])


# * Get all musics
@router.get("/all", response_model=list[music_schema.MusicOut])
def get_musics(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return music_services.get_musics(db=db, skip=skip, limit=limit)


# * Get specific user added musics
@router.get("/{user_id}", response_model=list[music_schema.MusicOut])
def get_user_added_musics(
    user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    db_user = user_services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    musics = music_services.get_user_added_musics(
        db=db, user_id=user_id, skip=skip, limit=limit
    )
    return musics


# * Updated music added by user
@router.put("/{music_id}", response_model=music_schema.MusicOut)
def update_music(
    music_id: int,
    updated_music: music_schema.MusicUpdate,
    db: Session = Depends(get_db),
    current_user: user_schema.UserOut = Depends(auth_services.get_current_user),
):
    music = music_services.get_music_by_id(db=db, music_id=music_id)
    if music is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Music not found"
        )
    if music.added_by != current_user["sub"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update the music you added",
        )
    return music_services.update_music(db=db, music_id=music_id, music=updated_music)


# * Remove music added by user
@router.delete("/{music_id}", response_model=music_schema.MusicOut)
def remove_music(
    music_id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.UserOut = Depends(auth_services.get_current_user),
):
    music = music_services.get_music_by_id(db=db, music_id=music_id)
    if music is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Music not found"
        )
    if music.added_by != current_user["sub"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete the music you added",
        )
    return music_services.remove_music(db=db, music_id=music_id)
