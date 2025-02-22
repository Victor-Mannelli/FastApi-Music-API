from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..config.config import Base

# Many-to-Many Relationship Table
user_music_association = Table(
    "user_music",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("music_id", Integer, ForeignKey("musics.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    musics = relationship("Music", secondary=user_music_association, back_populates="users")
    playlists = relationship("Playlist", back_populates="owner")

class Music(Base):
    __tablename__ = "musics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    artist = Column(String)

    users = relationship("User", secondary=user_music_association, back_populates="musics")

class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="playlists")

