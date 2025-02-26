import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.setup import Base  # Import your SQLAlchemy Base
from app.db.core import get_db  # Your dependency function for retrieving the DB session
from fastapi.testclient import TestClient
from app.main import app

# Use an in-memory SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the test database schema
@pytest.fixture(scope="function")
def db():
    Base.metadata.drop_all(bind=engine)  # Ensure a clean start
    Base.metadata.create_all(bind=engine)  # Create tables before each test
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)  # Clean up after each test

# Override FastAPI's get_db dependency to use the test database
@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
