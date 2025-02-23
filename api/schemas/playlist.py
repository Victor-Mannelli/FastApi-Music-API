from pydantic import BaseModel  # Import BaseModel, the foundation for Pydantic models
from typing import Optional  # Import Optional for fields that may be None
from .music import MusicBase


class PlaylistBase(BaseModel):
    name: str


class PlaylistUpdate(PlaylistBase):
    name: Optional[str] = None  # * Username can be updated but is optional


class PlaylistOutWithMusics(PlaylistBase):
    id: int  # * User ID is required in the response
    owner_id: int
    musics: Optional[list[MusicBase]]

    class Config:
        from_attributes = True  # * This allows Pydantic to read data from ORM models


class PlaylistOut(PlaylistBase):
    id: int  # * User ID is required in the response
    owner_id: int

    class Config:
        from_attributes = True  # This allows Pydantic to read data from ORM models
