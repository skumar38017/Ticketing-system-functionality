# app/workers/celery_app.py

from celery import Celery
from app.config import settings

celery_app = Celery(
    "ticket_management_system",
    broker=settings.RABBITMQ_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.task_routes = {
    "app.tasks.otp_task.*": {"queue": "otp_queue"},
    "app.tasks.payment_task.*": {"queue": "payment_queue"},
    "app.tasks.qr_task.*": {"queue": "qr_queue"},
}
# app/worker/celery_app.py
from app.workers.celery_app import celery_app

if __name__ == "__main__":
    celery_app.start()