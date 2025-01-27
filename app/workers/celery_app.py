# app/workers/celery_app.py

from celery import Celery
from app.config import config

celery_app = Celery(
    "ticket_management_system",
    broker=config.rabbitmq_url,
    backend=config.rabbitmq_result_backend,
)

# Task routing (queues)
celery_app.conf.task_routes = {
    "app.tasks.otp_task.*": {"queue": "otp_queue"},
    "app.tasks.payment_task.*": {"queue": "payment_queue"},
    "app.tasks.qr_task.*": {"queue": "qr_queue"},
    "app.tasks.email_tasks.*": {"queue": "email_queue"},
}

# Define Celery settings
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)