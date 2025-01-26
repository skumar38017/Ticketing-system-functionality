#  app/tasks/otp_task.py

from app.workers.celery_app import celery_app
from app.utils.message_service import send_sms
from app.utils.generate_otp import generate_otp

@celery_app.task
def send_otp_task(mobile_no: str):
    otp = generate_otp()
    send_sms(mobile_no, f"Your OTP is {otp}")
    # Store OTP in Redis for verification
    return {"message": "OTP sent"}
