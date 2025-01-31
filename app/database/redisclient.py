# app/database/redisclient.py
from redis import Redis
import logging
from app.config import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self):
        """
        Initialize Redis client with the broker URL from the configuration.
        """
        try:
            self.redis = Redis.from_url(config.redis_broker_url, decode_responses=True)
            logger.info("Redis client initialized.")
            print("Redis client initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize Redis client: {e}")
            raise

    def connect(self):
        """
        Connect to Redis and test the connection.
        """
        try:
            self.redis.ping()
            logger.info("Successfully connected to Redis.")
            print("Successfully connected to Redis.")
        except Exception as e:
            logger.error(f"Error connecting to Redis: {e}")
            raise

    def execute_command(self, *args, **kwargs):
        """
        Execute a Redis command.
        """
        try:
            result = self.redis.execute_command(*args, **kwargs)
            logger.info(f"Executed Redis command: {args[0]}")
            print(f"Executed Redis command: {args[0]}")
            return result
        except Exception as e:
            logger.error(f"Error executing Redis command {args[0]}: {e}")
            raise

    def disconnect(self):
        """
        Disconnect from Redis gracefully.
        """
        try:
            self.redis.close()
            logger.info("Disconnected from Redis.")
            print("Disconnected from Redis.")
        except Exception as e:
            logger.error(f"Error disconnecting from Redis: {e}")
            raise

    def get_redis_status(self):
        """
        Fetch and print Redis server status.
        """
        try:
            # Fetch general information about Redis server
            info = self.redis.info()
            logger.info(f"Redis Server Information: {info}")
            print("Redis Server Information:")
            for key, value in info.items():
                print(f"{key}: {value}")
        except Exception as e:
            logger.error(f"Error fetching Redis status: {e}")
            raise

    def get_active_clients(self):
        """
        Fetch and print active Redis clients.
        """
        try:
            # Get the list of connected clients
            clients = self.redis.client_list()
            logger.info(f"Active Redis Clients: {clients}")
            print("Active Redis Clients:")
            for client in clients:
                print(client)
        except Exception as e:
            logger.error(f"Error fetching active Redis clients: {e}")
            raise

# Create a RedisClient instance
redis_client = RedisClient()