from app.config.setup import AsyncSessionLocal


async def get_async_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
