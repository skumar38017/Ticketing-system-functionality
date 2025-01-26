#  app/database/database.py

import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import config

def get_db_connection():
    db_url = psycopg2.connect(
        db_url=config.database_url,
    )
    return db_url