from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..services import playlist as playlist_services
from ..services import music as music_services
from ..services import auth as auth_services
from ..schemas import playlist as playstlist_schema
from ..schemas import user as user_schema
from ..db.core import get_async_db

router = APIRouter(prefix="/playlist")


# * Create a playlist
@router.post("", response_model=playstlist_schema.PlaylistOut)
async def create_playlist(
    playlist: playstlist_schema.PlaylistBase,
    db: Session = Depends(get_async_db),
    current_user: user_schema.UserOut = Depends(auth_services.get_current_user),
):
    # * there is no need to check if current user exists because the get_current_user function already does that
    return await playlist_services.create_playlist(
        db=db, playlist=playlist, user_id=current_user.id
    )


# * Add music to a user playlist
@router.post(
    "/{playlist_id}/add-music/{music_id}", response_model=playstlist_schema.PlaylistOut
)
async def add_music_to_playlist(
    playlist_id: int,
    music_id: int,
    db: Session = Depends(get_async_db),
    current_user: user_schema.UserOut = Depends(auth_services.get_current_user),
):
    playlist = await playlist_services.get_playlist_by_id(
        db=db, playlist_id=playlist_id
    )
    music = await music_services.get_music_by_id(db=db, music_id=music_id)
    if not playlist or not music:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Playlist or music not found"
        )
    if playlist.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only add music to your own playlists",
        )
    return await playlist_services.add_music_to_playlist(
        db=db, music_id=music_id, playlist_id=playlist_id
    )


# * Get all user playlists
@router.get("/from-user/{user_id}", response_model=list[playstlist_schema.PlaylistOut])
async def get_user_playlists(user_id: int, db: Session = Depends(get_async_db)):
    return await playlist_services.get_user_playlists(db=db, user_id=user_id)


# * Get musics by playlist
@router.get(
    "/{playlist_id}/musics", response_model=playstlist_schema.PlaylistOutWithMusics
)
async def get_playlist_musics(playlist_id: int, db: Session = Depends(get_async_db)):
    return await playlist_services.get_playlist_musics(db=db, playlist_id=playlist_id)


# * Remove music from playlist
@router.put(
    "/{playlist_id}/remove-music/{music_id}",
    response_model=playstlist_schema.PlaylistOutWithMusics,
)
async def remove_music_from_playlist(
    playlist_id: int,
    music_id: int,
    db: Session = Depends(get_async_db),
    current_user: user_schema.UserOut = Depends(auth_services.get_current_user),
):
    playlist = await playlist_services.get_playlist_by_id(
        db=db, playlist_id=playlist_id
    )
    music = await music_services.get_music_by_id(db=db, music_id=music_id)
    if not playlist or not music:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Playlist or music not found"
        )
    if playlist.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only remove music from your own playlists",
        )
    return await playlist_services.remove_music_from_playlist(
        db=db, music_id=music_id, playlist_id=playlist_id
    )


@router.put("/{playlist_id}", response_model=playstlist_schema.PlaylistOut)
async def update_playlist(
    playlist_id: int,
    updated_playlist: playstlist_schema.PlaylistUpdate,
    db: Session = Depends(get_async_db),
    current_user: user_schema.UserOut = Depends(auth_services.get_current_user),
):
    playlist = await playlist_services.get_playlist_by_id(
        db=db, playlist_id=playlist_id
    )
    if playlist.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own playlists",
        )
    return await playlist_services.update_playlist(
        db=db, playlist_id=playlist_id, playlist=updated_playlist
    )


# * Deletes user playlist
@router.delete("/{playlist_id}", response_model=playstlist_schema.PlaylistOut)
async def delete_playlist(
    playlist_id: int,
    db: Session = Depends(get_async_db),
    current_user: user_schema.UserOut = Depends(auth_services.get_current_user),
):
    playlist = await playlist_services.get_playlist_by_id(
        db=db, playlist_id=playlist_id
    )
    if playlist.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own playlists",
        )
    return await playlist_services.delete_playlist(db=db, playlist_id=playlist_id)
