from sqlalchemy import Column, Integer, String, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from app.config.setup import Base

# Many-to-Many Relationship Table between Playlist and Music
playlist_music_association = Table(
    "playlist_music",
    Base.metadata,
    Column(
        "playlist_id",
        Integer,
        ForeignKey("playlists.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "music_id",
        Integer,
        ForeignKey("musics.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # Songs added by the user
    added_musics = relationship(
        "Music", back_populates="added_by_user", cascade="all, delete"
    )

    # Playlists the user owns
    playlists = relationship("Playlist", back_populates="owner", cascade="all, delete")


class Music(Base):
    __tablename__ = "musics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    artist = Column(String, index=True)
    link = Column(String)
    added_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    __table_args__ = (UniqueConstraint("title", "artist", name="_title_artist_uc"),)

    # User who added the song
    added_by_user = relationship("User", back_populates="added_musics")

    # Playlists this song belongs to
    # secondary means it's a many to many relation that is using another table for relation
    playlists = relationship(
        "Playlist", secondary=playlist_music_association, back_populates="musics"
    )


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    # The user who owns the playlist
    owner = relationship("User", back_populates="playlists")

    # Songs that are in this playlist
    musics = relationship(
        "Music", secondary=playlist_music_association, back_populates="playlists"
    )
