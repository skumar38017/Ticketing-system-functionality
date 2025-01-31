# app/workers/celery_app.py
from celery import Celery
from app.config import config
from celery.signals import after_task_publish, worker_ready


# Initialize the Celery application
celery_app = Celery(
    "ticket_management_system",
    broker=config.rabbitmq_url,
    backend=config.rabbitmq_result_backend,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    broker_connection_retry_on_startup=True,
    task_default_queue="default",
    task_routes={
        "app.tasks.otp_task.*": {"queue": "otp_queue"},
        "app.tasks.payment_task.*": {"queue": "payment_queue"},
        "app.tasks.qr_task.*": {"queue": "qr_queue"},
        "app.tasks.email_tasks.*": {"queue": "email_queue"},
    },
)


# Autodiscover tasks in the project
celery_app.autodiscover_tasks(["app.tasks"], force=True)

@worker_ready.connect
def on_worker_ready(sender, **kwargs):
    """
    Signal handler for when a worker is ready.
    This can be used to trigger initial tasks or perform setup actions.
    """
    print("Worker ready")