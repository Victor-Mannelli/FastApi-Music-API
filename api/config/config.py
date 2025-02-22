import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv() # Loads environment variables from .env

DATABASE_URL = os.getenv("DATABASE_URL") # Fetches the DB connection from the env variable
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Check your .env file.")


engine = create_engine(DATABASE_URL) # Creates the connection to PostgreSQL.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Used to interact with the DB.
Base = declarative_base() # The base class for defining models.
