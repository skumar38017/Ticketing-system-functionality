#  Neon-Stdio-Holi-T25/app/config.py

from app.settings import settings
from typing import Dict

class Config:
    """
    Application configuration manager.

    Provides properties for:
    - Database URLs (sync/async)
    - RabbitMQ URL
    - Redis URLs
    - Celery configuration
    - General app settings (CORS, debug, etc.)
    - Webhook, SMS, and OTP configurations
    - Email settings
    """

    # Database URLs
    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
            f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
        )

    @property
    def async_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
            f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
        )

    # RabbitMQ URL
    @property
    def rabbitmq_url(self) -> str:
        return (
            f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@"
            f"{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}/{settings.RABBITMQ_VHOST}"
        )

    @property
    def rabbitmq_result_backend(self) -> str:
        return settings.CELERY_RESULT_BACKEND
    
    # Redis URLs
    @property
    def redis_broker_url(self) -> str:
        return f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB_BROKER}"

    @property
    def redis_result_url(self) -> str:
        return f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB_RESULT}"

    # Celery configuration
    @property
    def celery_broker_url(self) -> str:
        return settings.CELERY_BROKER_URL

    @property
    def celery_result_backend(self) -> str:
        return settings.CELERY_RESULT_BACKEND

    # General App Configurations
    @property
    def app_config(self) -> Dict[str, str]:
        return {
            "debug": settings.DEBUG,
            "host": settings.HOST,
            "port": settings.PORT,
            "allowed_hosts": settings.ALLOWED_HOSTS,
            "secret_key": settings.SECRET_KEY,
            "cors_origins": settings.CORS_ORIGINS,
            "dev_mode": settings.DEV_MODE,
        }

    # Webhook URL
    @property
    def webhook_url(self) -> str:
        return settings.WEBHOOK_URL

    # SMS Configuration
    @property
    def sms_api(self) -> Dict[str, str]:
        return {
            "url": settings.SMS_API_URL,
            "key": settings.SMS_API_KEY,
        }

    # OTP Expiration Time
    @property
    def otp_expiration_time(self) -> int:
        return settings.OTP_EXPIRATION_TIME

    # Email Settings
    @property
    def email_address(self) -> str:
        return settings.EMAIL_ADDRESS

    @property
    def email_password(self) -> str:
        return settings.EMAIL_PASSWORD


# Export a single Config instance for global access
config = Config()
