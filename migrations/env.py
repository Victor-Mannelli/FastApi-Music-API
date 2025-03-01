from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from logging.config import fileConfig

# Import models to make sure Alembic knows about them
from app.db.models import User, Music, Playlist
from app.config.setup import DATABASE_URL, Base
from alembic import context

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Check your .env file.")

# Alembic Config object
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata  # Alembic needs this to detect changes in your models


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())
