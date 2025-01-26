#  app/database/redisclient.py

from app.config import config
from redis import Redis

class RedisClient:
    """
    Redis client for managing Redis connections.

    - Provides methods for connecting to Redis, executing commands, and disconnecting.
    - Uses `settings` from `app.config.settings` for Redis URLs.
    """

    def __init__(self):
        self.redis = Redis.from_url(config.redis_broker_url)

    def connect(self):
        """
        Connect to Redis.
        """
        self.redis.connect()

    def execute_command(self, *args, **kwargs):
        """
        Execute a Redis command.

        Args:
            *args: Positional arguments for the Redis command.
            **kwargs: Keyword arguments for the Redis command.

        Returns:
            The result of the Redis command execution.
        """
        return self.redis.execute_command(*args, **kwargs)

    def disconnect(self):
        """
        Disconnect from Redis.
        """
        self.redis.disconnect()  # Close the connection