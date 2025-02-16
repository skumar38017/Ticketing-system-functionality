#  app/migrations/env.py

from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from alembic import context
from app.config import config
from app.database.base import Base  
from app.database import models  # Import your models so Alembic can detect them
target_metadata = Base.metadata

# Alembic config object
alembic_config = context.config

# Apply logging configuration
if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

# Set the target metadata for 'autogenerate' support
target_metadata = Base.metadata

# Set database URL dynamically from the config
alembic_config.set_main_option("sqlalchemy.url", config.async_database_url)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = alembic_config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Helper function to run migrations."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(
        alembic_config.get_main_option("sqlalchemy.url"),
        future=True,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
