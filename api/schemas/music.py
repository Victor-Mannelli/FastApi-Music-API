from pydantic import BaseModel  # Import BaseModel, the foundation for Pydantic models
from typing import Optional  # Import Optional for fields that may be None


class MusicBase(BaseModel):
    title: str
    artist: str
    link: str


class MusicUpdate(MusicBase):
    title: Optional[str] = None  # Username can be updated but is optional
    artist: Optional[str] = None  # Email can be updated but is optional
    link: Optional[str] = None  # Email can be updated but is optional


class MusicOut(MusicBase):
    id: int
    added_by: int

    class Config:
        from_attributes = True
