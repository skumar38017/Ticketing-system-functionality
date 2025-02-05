# app/database/database.py

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import logging
import asyncio
from app.config import config
from typing import AsyncGenerator  # Import AsyncGenerator from typing

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Fixing the return type to be an async generator
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get an async session for the database.
    This function is now correctly typed as an async generator.
    """
    db = SessionLocal()  # Create the async session
    try:
        yield db  # Yield the session to FastAPI for dependency injection
    finally:
        await db.close()  # Close the session after the request is handled

# Provide an alias for get_db
get_db_connection = get_db

async def login_to_database():
    """
    Try to log in by connecting to the database using the provided URL.
    This function only checks if the connection can be established, without running any queries.
    """
    try:
        # Attempt to connect to the database
        async with engine.connect() as connection:
            # Simply open and close the connection to check if it's working
            logger.info("Successfully connected to the database.")
            print(f"Successfully connected to the async database.{config.async_database_url}")
            print(f"Successfully connected to the sync database.{config.database_url}")
    except OperationalError as e:
        logger.error(f"Database connection failed: {e}")
        print(f"Database connection failed: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")

# Run the login function asynchronously
async def main():
    await login_to_database()


if __name__ == "__main__":
    asyncio.run(main())