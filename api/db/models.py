from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..config.setup import Base

# Many-to-Many Relationship Table between User and Music (for stored songs)
user_music_association = Table(
    "user_music",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("music_id", Integer, ForeignKey("musics.id"), primary_key=True),
)
# Many-to-Many Relationship Table between Playlist and Music
playlist_music_association = Table(
    "playlist_music",
    Base.metadata,
    Column("playlist_id", Integer, ForeignKey("playlists.id"), primary_key=True),
    Column("music_id", Integer, ForeignKey("musics.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # Songs the user has stored
    musics = relationship(
        "Music", secondary=user_music_association, back_populates="users"
    )
    # Playlists the user owns
    playlists = relationship("Playlist", back_populates="owner")


class Music(Base):
    __tablename__ = "musics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    artist = Column(String)
    link = Column(String)
    added_by = Column(Integer, ForeignKey("users.id"))

    # Users who have saved this song
    users = relationship(
        "User", secondary=user_music_association, back_populates="musics"
    )
    # Playlists this song belongs to
    playlists = relationship(
        "Playlist", secondary=playlist_music_association, back_populates="musics"
    )


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # The user who owns the playlist
    owner = relationship("User", back_populates="playlists")
    # Songs that are in this playlist
    musics = relationship(
        "Music", secondary=playlist_music_association, back_populates="playlists"
    )
