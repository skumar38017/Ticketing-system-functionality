# app/utils/redis_data_storage.py

import json
import hashlib
from typing import Optional
from app.config import config
from app.database.redisclient import redis_client

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

            # Store  hashed version data in Redis
            redis_client.execute_command('SETEX', key, expiration, json.dumps({
                "original_data": data_with_session,
                "hashed_data": hashed_data
            }))
        except Exception as e:
            print(f"Error storing data in Redis: {e}")
            raise
        
    @staticmethod
    def get_data_from_redis(key: str) -> Optional[dict]:
        """
        Retrieve data from Redis using the key. If the data is hashed, return the original data.

        Args:
            key (str): The key to retrieve data from Redis.

        Returns:
            dict: The original data if hash matches, or None if not found.
        """
        try:
            data = redis_client.execute_command('GET', key)
            
            if data:
                # Parse the stored data from JSON
            
                stored_data = json.loads(data.decode())
                original_data = stored_data.get("original_data")
                hashed_data = stored_data.get("hashed_data")
                
                # Verify if the hash of the original data matches the stored hash
                combined_data = json.dumps(original_data)
                
                if RedisDataStorage.hash_data(combined_data) == hashed_data:
                    return combined_data  # Return the original data if the hash matches
                
                else:
                    print("Data integrity check failed: Hash mismatch")
                    return None  # Hash mismatch, return None
        
            return None
        
        except Exception as e:
            print(f"Error retrieving data from Redis: {e}")
            return None