from app.tasks.otp_task import send_otp_task
from celery.result import AsyncResult
from app.workers.celery_app import celery_app

def test_send_otp_task():
    """
    Test function to trigger the send_otp_task Celery task.
    """
    try:
        phone_no = "+1234567890"
        name = "John Doe"
        otp = "123456"

        print(f"Triggering OTP task for {phone_no}...")
        task = send_otp_task.delay(phone_no, name, otp)  # .delay() is valid for a registered Celery task.

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

if __name__ == "__main__":
    test_send_otp_task()