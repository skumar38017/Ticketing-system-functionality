#  Neon-Stdio-Holi-T25/app/config.py

from app.settings import settings

class Config:
    """
    Application configuration manager.

    - Provides properties for database URLs, RabbitMQ URL, Redis URLs,
      Celery configuration, general app configurations, webhook URL,
      SMS configuration, and OTP expiration time.
    - Leverages `settings` from `app.settings.py` for environment variable access.
    """

    # Database URLs
    @property
    def database_url(self):
        return f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

    @property
    def async_database_url(self):
        return f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

    # RabbitMQ URL
    @property
    def rabbitmq_url(self):
        return f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}/{settings.RABBITMQ_VHOST}"

    # Redis URLs
    @property
    def redis_broker_url(self):
        return f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB_BROKER}"

    @property
    def redis_result_url(self):
        return f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB_RESULT}"

    # Celery Configuration
    @property
    def celery_broker_url(self):
        return settings.CELERY_BROKER_URL

    @property
    def celery_result_backend(self):
        return settings.CELERY_RESULT_BACKEND

    # General App Configurations
    @property
    def app_config(self):
        return {
            "debug": settings.DEBUG,
            "host": settings.HOST,
            "port": settings.PORT,
            "allowed_hosts": settings.ALLOWED_HOSTS,
            "secret_key": settings.SECRET_KEY,
        }

    # Webhook Configuration
    @property
    def webhook_url(self):
        return settings.WEBHOOK_URL

    # SMS Configuration
    @property
    def sms_api(self):
        return {
            "url": settings.SMS_API_URL,
            "key": settings.SMS_API_KEY,
        }

    # OTP Expiration Time
    @property
    def otp_expiration_time(self):
        return settings.OTP_EXPIRATION_TIME


    # Email Settings
    @property
    def email_address(self):
        return settings.EMAIL_ADDRESS
    @property
    def email_password(self):
        return settings.EMAIL_PASSWORD  
    
# Export a single Config instance for global access
config = Config()
