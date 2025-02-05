import sys
import os
from time import sleep
from celery.result import AsyncResult

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.tasks.otp_task import send_otp_task
from app.workers.celery_app import celery_app  # Ensure app is correctly imported

def test_send_otp_task():
    """
    Test function to trigger the send_otp_task Celery task.
    """
    try:
        phone_no = "+919876543210"
        name = "Sumit ji"
        otp = "123456"  # Make sure to pass this argument to the task

        print(f"Triggering OTP task for {phone_no}...")
        task = send_otp_task.delay(phone_no, name, otp)  # Provide required arguments

        print(f"Task ID: {task.id}")

        # Wait for the task to complete
        task_result = None
        while task_result is None:
            sleep(1)  # Wait for the task to complete
            task_result = AsyncResult(task.id)  # No need to pass celery_app here
            print(f"Task Status: {task_result.status}")

        if task_result.status == "SUCCESS":
            print(f"Task Result: {task_result.result}")
        else:
            print(f"Task Failed: {task_result.traceback}")
       
    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    test_send_otp_task()
