# app/workers/celery_app.py

from celery import Celery
from app.config import config

# Initialize the Celery application
celery_app = Celery(
    "ticket_management_system",
    broker=config.rabbitmq_url,  # RabbitMQ URL from config
    backend=config.rabbitmq_result_backend,  # Result backend URL from config
)

# Configure Celery settings
celery_app.conf.update(
    task_serializer="json",  # Serialize tasks using JSON
    accept_content=["json"],  # Accept only JSON-serialized tasks
    result_serializer="json",  # Serialize results in JSON format
    timezone="UTC",  # Set the timezone
    enable_utc=True,  # Enable UTC for consistent time management
)

# Configure task routing (queues)
celery_app.conf.task_routes = {
    "app.tasks.otp_task.*": {"queue": "otp_queue"},  # OTP-related tasks routed to 'otp_queue'
    "app.tasks.payment_task.*": {"queue": "payment_queue"},  # Payment-related tasks routed to 'payment_queue'
    "app.tasks.qr_task.*": {"queue": "qr_queue"},  # QR code-related tasks routed to 'qr_queue'
    "app.tasks.email_tasks.*": {"queue": "email_queue"},  # Email-related tasks routed to 'email_queue'
}

# Autodiscover tasks in the project
celery_app.autodiscover_tasks(["app.tasks"])
