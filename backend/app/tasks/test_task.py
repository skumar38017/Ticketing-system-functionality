import sys
import os
from time import sleep
from celery.result import AsyncResult

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.workers.celery_app import celery_app  # Ensure app is correctly imported


def test_send_otp_task():
    """
    Test function to trigger the send_otp_task Celery task.
    """
    try:
        phone_no = "+919876543210"
        name = "Sumit ji"
        otp = "123456"

        print(f"Triggering OTP task for {phone_no}...")
        task_result = celery_app.send_task(
            "app.tasks.otp_task.send_otp_task", args=[phone_no, name, otp]
        )

        print(f"Task ID: {task_result.id}")

        # Check task status until completion
        while not task_result.ready():
            print(f"Task Status: {task_result.status}")
            sleep(1)  # Wait 1 second before checking again

        # Task completed, display the result or error
        if task_result.status == "SUCCESS":
            print(f"Task Result: {task_result.result}")
        else:
            print(f"Task Failed: {task_result.status}")
            if task_result.traceback:
                print(f"Error Traceback: {task_result.traceback}")

    except Exception as e:
        print(f"Error during testing: {str(e)}")


if __name__ == "__main__":
    test_send_otp_task()
