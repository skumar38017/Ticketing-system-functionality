from celery import Celery
from app.config import config
from app.email_utils import send_email

celery = Celery('tasks', broker=config.CELERY_BROKER_URL)

@celery.task
def send_welcome_email(user_email: str, qr_code_image: bytes):
    print('send_welcome_email user_email', user_email)
    send_email(user_email, qr_code_image)
