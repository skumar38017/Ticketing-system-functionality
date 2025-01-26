# app/database/redisclient.py
from app.config import config
from redis import Redis
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self):
        # Initialize Redis client with Redis broker URL from config
        self.redis = Redis.from_url(config.redis_broker_url)
        logger.info("Redis client initialized.")

    def connect(self):
        """
        Connect to Redis and check the connection status.
        """
        try:
            self.redis.ping()  # Test the connection to Redis
            logger.info("Connected to Redis.")
        except Exception as e:
            logger.error(f"Error connecting to Redis: {e}")
            raise

    def execute_command(self, *args, **kwargs):
        """
        Execute a Redis command.
        """
        try:
            return self.redis.execute_command(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error executing Redis command: {e}")
            raise

    def disconnect(self):
        """
        Disconnect from Redis gracefully.
        """
        try:
            self.redis.close()  # Close the Redis connection
            logger.info("Disconnected from Redis.")
        except Exception as e:
            logger.error(f"Error disconnecting from Redis: {e}")
            raise
