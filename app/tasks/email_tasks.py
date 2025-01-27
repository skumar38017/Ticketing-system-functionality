# app/tasks/email_tasks.py
from celery import Celery
from app.config import config
from app.workers.celery_app import celery_app
from app.utils.email_utils import send_email

celery = Celery('tasks', broker=config.CELERY_BROKER_URL)

@celery_app.task
def send_welcome_email(user_email: str, qr_code_image: bytes):
    """
    Sends a welcome email with the attached QR code.
    
    Args:
        user_email (str): The recipient's email address.
        qr_code_image (bytes): The QR code image to be attached.
    """
    send_email(user_email, qr_code_image)
    print('Sending welcome email to:', send_email)
    return {"message": f"Email sent to {user_email}"}