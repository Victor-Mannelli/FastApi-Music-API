import os
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()  # Loads environment variables from .env

DATABASE_URL = os.getenv("DATABASE_URL")
# Fetches the DB connection from the env variable
JWT_SECRET = os.getenv("JWT_SECRET")
# Fetches the JWT_SECRET from the env variable
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Check your .env file.")


engine = create_engine(DATABASE_URL)  # Creates the connection to PostgreSQL.
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  # Used to interact with the DB.
Base = declarative_base()  # The base class for defining models.
