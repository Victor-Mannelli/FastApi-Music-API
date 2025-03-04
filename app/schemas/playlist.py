from pydantic import BaseModel  # Import BaseModel, the foundation for Pydantic models
from typing import Optional  # Import Optional for fields that may be None
from .music import MusicOut


class PlaylistBase(BaseModel):
    name: str
    private: bool = False


class PlaylistUpdate(PlaylistBase):
    name: Optional[str] = None  # * Username can be updated but is optional
    private: Optional[bool] = None


class PlaylistOutWithMusics(PlaylistBase):
    id: int  # * User ID is required in the response
    owner_id: int
    private: bool
    musics: Optional[list[MusicOut]]

    class Config:
        from_attributes = True  # * This allows Pydantic to read data from ORM models


class AddedMusicToPlaylist(BaseModel):
    artist: str
    title: str
    added_by: int
    id: int
    link: str


class PlaylistOut(PlaylistBase):
    id: int  # * User ID is required in the response
    owner_id: int
    private: bool

    class Config:
        from_attributes = True  # This allows Pydantic to read data from ORM models
