#  app/database/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import config
from sqlalchemy.exc import OperationalError
import logging
import asyncio

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


#  
async def login_to_database():
    """
    Try to log in by connecting to the database using the provided URL.
    This function only checks if the connection can be established, without running any queries.
    """
    try:
        # Attempt to connect to the database
        async with engine.connect() as connection:
            # Simply open and close the connection to check if it's working
            pass  # No SQL query is executed
        logger.info("Successfully connected to the database.")
        print("Successfully connected to the database.")
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