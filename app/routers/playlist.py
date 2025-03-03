from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from ..services import playlist as playlist_services
from ..services import music as music_services
from ..services import auth as auth_services
from ..schemas import playlist as playstlist_schema
from ..schemas import music as music_schema
from ..schemas import user as user_schema
from ..db.core import get_async_db

router = APIRouter(prefix="/playlist")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# * Create a playlist
@router.post(
    "",
    response_model=playstlist_schema.PlaylistOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_playlist(
    playlist: playstlist_schema.PlaylistBase,
    db: AsyncSession = Depends(get_async_db),
    current_user: user_schema.UserOut = Depends(auth_services.get_current_user),
):
    # * there is no need to check if current user exists because the get_current_user function already does that
    return await playlist_services.create_playlist(
        db=db, playlist=playlist, user_id=current_user.id
    )


# * Add music to a user playlist
@router.post(
    "/{playlist_id}/add-music/{music_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=music_schema.MusicOut,
)
async def add_music_to_playlist(
    playlist_id: int,
    music_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: user_schema.UserOut = Depends(auth_services.get_current_user),
):
    return await playlist_services.add_music_to_playlist(
        requester_id=current_user.id,
        playlist_id=playlist_id,
        music_id=music_id,
        db=db,
    )


# * Get all user playlists
@router.get("/from-user/{user_id}", response_model=list[playstlist_schema.PlaylistOut])
async def get_user_playlists(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: Optional[user_schema.UserOut] = Depends(
        auth_services.get_optional_current_user
    ),
):
    return await playlist_services.get_user_playlists(
        requester_id=current_user.id if current_user else None,
        user_id=user_id,
        db=db,
    )


# * Get musics by playlist
@router.get(
    "/{playlist_id}/musics", response_model=playstlist_schema.PlaylistOutWithMusics
)
async def get_playlist_musics(
    playlist_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: Optional[user_schema.UserOut] = Depends(
        auth_services.get_optional_current_user
    ),
):
    return await playlist_services.get_playlist_musics(
        requester_id=current_user.id if current_user else None,
        playlist_id=playlist_id,
        db=db,
    )


# * Remove music from playlist
@router.put(
    "/{playlist_id}/remove-music/{music_id}",
    response_model=playstlist_schema.PlaylistOutWithMusics,
)
async def remove_music_from_playlist(
    playlist_id: int,
    music_id: int,
    db: AsyncSession = Depends(get_async_db),
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
    db: AsyncSession = Depends(get_async_db),
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
    db: AsyncSession = Depends(get_async_db),
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
