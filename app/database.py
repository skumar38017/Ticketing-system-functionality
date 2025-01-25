import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import config

def get_db_connection():
    conn = psycopg2.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST
    )
    return conn
