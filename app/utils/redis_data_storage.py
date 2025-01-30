# app/utils/redis_data_storage.py

import json
import hashlib
from typing import Optional
from app.database.redisclient import redis_client  # Import the redis_client instance
from app.config import config

class RedisDataStorage:
    """
    A class to handle Redis data storage operations, including hashing and session management.
    """

    @staticmethod
    def hash_data(data: str) -> str:
        """
        Hash the input data using SHA-256.

        Args:
            data (str): The data to hash.

        Returns:
            str: The hashed value as a hexadecimal string.
        """
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def generate_redis_key(name: str, email: str, phone_no: str) -> str:
        """
        Generate a unique Redis key by hashing the combination of name, email, and phone number.

        Args:
            name (str): The name of the user.
            email (str): The email of the user.
            phone_no (str): The phone number of the user.

        Returns:
            str: The generated Redis key.
        """
        combined_data = f"{name}_{email}_{phone_no}"
        return f"user_data_{RedisDataStorage.hash_data(combined_data)}"

    @staticmethod
    def store_data_in_redis(key: str, data: dict, session_id: str, expiration: int = config.expiration_time) -> None:
        """
        Store hashed data in Redis with an expiration time and session information.
    
        Args:
            key (str): The key under which data will be stored.
            data (dict): The data to store.
            session_id (str): The current user's session ID.
            expiration (int): The expiration time in seconds (default is 5 minutes).
    
        Raises:
            Exception: If an error occurs while storing data in Redis.
        """
        try:
            # Add session information to the data
            data_with_session = {**data, "session": session_id}
    
            # Convert the combined data to JSON and hash it
            combined_data = json.dumps(data_with_session)
            hashed_data = RedisDataStorage.hash_data(combined_data)
    
            # Store the hashed data in Redis
            redis_client.execute_command('SETEX', key, expiration, hashed_data)
        except Exception as e:
            print(f"Error storing data in Redis: {e}")
            raise
    @staticmethod
    def get_data_from_redis(key: str) -> Optional[dict]:
        """
        Retrieve hashed data from Redis using the key.

        Args:
            key (str): The key to retrieve data from Redis.

        Returns:
            dict: The data stored in Redis, or None if not found.
        """
        try:
            hashed_data = redis_client.execute_command('GET', key)
            if hashed_data:
                # Since the data is hashed, you cannot directly decode it back to the original dictionary.
                # You can only verify if the data matches a given input by hashing the input and comparing.
                # For this example, we return the hashed data as-is.
                return {"hashed_data": hashed_data.decode()}  # Return the hashed data
            return None
        except Exception as e:
            print(f"Error retrieving data from Redis: {e}")
            return None