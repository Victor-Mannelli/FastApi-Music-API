import logging
from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from api.config import SessionLocal
from .routers.user import router as users_router
from .routers.music import router as musics_router
from .routers.playlist import router as playlists_router

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(users_router)
app.include_router(musics_router)
app.include_router(playlists_router)


@app.get("/health")
def health_check():
    try:
        # Using a context manager to automatically close the session
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))  # Running a raw SQL query with text()
        return {"status": "Database connected!"}
    except Exception as e:
        # Log the exception details
        logger.error(f"Error connecting to the database: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Database connection failed: {str(e)}"
        )
