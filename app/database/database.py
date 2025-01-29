#  app/database/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Database connection established.")

# Create async SQLAlchemy engine
engine = create_async_engine(config.async_database_url, echo=True)

# Async sessionmaker for database transactions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

# Base class for models
Base = declarative_base()

async def get_db():
    """
    Dependency to get an async session for the database.
    """
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()  # Properly close the async session

# Provide an alias for get_db
get_db_connection = get_db
