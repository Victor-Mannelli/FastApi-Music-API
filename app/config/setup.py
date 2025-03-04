import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()  # Loads environment variables from .env

DATABASE_URL = os.getenv("DATABASE_URL")
# Fetches the DB connection from the env variable
JWT_SECRET = os.getenv("JWT_SECRET")
# Fetches the JWT_SECRET from the env variable
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
ALGORITHM = os.getenv("ALGORITHM")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Check your .env file.")


# Creates the connection to PostgreSQL.
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()  # The base class for defining models.
