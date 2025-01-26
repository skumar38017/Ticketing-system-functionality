#  app/database/database.py

# app/database/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import config

# Create SQLAlchemy engine
engine = create_engine(config.async_database_url, echo=True)

# SessionLocal: Session for database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_="AsyncSession")

Base = declarative_base()

def get_db():
    """
    Dependency to get a session for the database
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
