# app/tasks/test_task.py

from app.tasks.otp_task import send_otp_task
from celery.result import AsyncResult
from app.workers.celery_app import celery_app

def test_send_otp_task():
    """
    Test function to trigger the send_otp_task Celery task.
    """
    try:
        phone_no = "+917463061636"
        name = "Sumit ji"
        otp = "123456"

        print(f"Triggering OTP task for {phone_no}...")
        task = send_otp_task.delay(phone_no, name, otp)  # Provide required arguments

        print(f"Task ID: {task.id}")

        # Use AsyncResult to monitor the task
        result = AsyncResult(task.id, app=celery_app)
        print(f"Task Status: {result.status}")

        if result.status == "SUCCESS":
            print(f"Task Result: {result.result}")
        else:
            print(f"Task Failed: {result.traceback}")
    
    except Exception as e:
        print(f"Error during testing: {str(e)}")