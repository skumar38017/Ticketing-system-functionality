#  app/settings.py

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Settings:
    """
    Application configuration settings.

    - Leverages environment variables for flexibility and security.
    - Provides clear and descriptive variable names.
    - Uses type hints for better code readability and maintainability.
    """

    # General Settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default_secret_key")
    ALLOWED_HOSTS: list[str] = os.getenv("ALLOWED_HOSTS", "*").split(",")

    # Database
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "postgres")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))

    # RabbitMQ
    RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST", "localhost")
    RABBITMQ_USER: str = os.getenv("RABBITMQ_USER", "guest")
    RABBITMQ_PASSWORD: str = os.getenv("RABBITMQ_PASSWORD", "guest")
    RABBITMQ_PORT: int = int(os.getenv("RABBITMQ_PORT", 5672))
    RABBITMQ_VHOST: str = os.getenv("RABBITMQ_VHOST", "/")

    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB_BROKER: int = int(os.getenv("REDIS_DB_BROKER", 0))
    REDIS_DB_RESULT: int = int(os.getenv("REDIS_DB_RESULT", 0))

    # Celery
    CELERY_BROKER_URL: str = os.getenv(
        "CELERY_BROKER_URL",
        f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}"
    )
    CELERY_RESULT_BACKEND: str = os.getenv(
        "CELERY_RESULT_BACKEND",
        f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_RESULT}"
    )

    # Webhook
    WEBHOOK_URL: str = os.getenv("WEBHOOK_URL", "http://localhost:8000/webhook/payment")

    # SMS Service
    SMS_API_URL: str = os.getenv("SMS_API_URL", "https://api.smsprovider.com/send")
    SMS_API_KEY: str = os.getenv("SMS_API_KEY", "your_sms_api_key")

    # OTP Settings
    OTP_EXPIRATION_TIME: int = int(os.getenv("OTP_EXPIRATION_TIME", 300))


# Export an instance of Settings
settings = Settings()