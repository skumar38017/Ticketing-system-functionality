#  app/utils/redis.py

import json
from typing import Optional
from app.database.redisclient import redis_client  # Import the redis_client instance from redisclient.py
from app.config import config

def store_data_in_redis(key: str, data: dict, expiration: int = config.expiration_time) -> None:
    """
    Store data in Redis with an expiration time.

    Args:
        key (str): The key under which data will be stored (usually a user or phone number).
        data (dict): The data to store.
        expiration (int): The expiration time in seconds (default is 5 minutes).
    """
    # Convert data to JSON before storing it in Redis
    try:
        # Using RedisClient's execute_command to set the key-value pair
        redis_client.execute_command('SETEX', key, expiration, json.dumps(data))
    except Exception as e:
        # Handle any errors that might occur during the operation
        print(f"Error storing data in Redis: {e}")
        raise

def get_data_from_redis(key: str) -> Optional[dict]:
    """
    Retrieve data from Redis using the key.

    Args:
        key (str): The key to retrieve data from Redis.

    Returns:
        dict: The data stored in Redis, or None if not found.
    """
    try:
        # Using RedisClient's execute_command to get the value for the key
        data = redis_client.execute_command('GET', key)
        if data:
            return json.loads(data)  # Convert from JSON back to dictionary
        return None
    except Exception as e:
        # Handle any errors that might occur during the operation
        print(f"Error retrieving data from Redis: {e}")
        return None