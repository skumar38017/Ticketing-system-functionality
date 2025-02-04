# app/tasks/otp_task.py
from celery import shared_task
import logging
import requests
from app.config import config
from celery.signals import task_prerun
from celery.exceptions import MaxRetriesExceededError
from app.services.websocket_service import WebSocketHandler

# Initialize logger
logger = logging.getLogger("celery.task")

# This handler listens for the task execution event (before task starts)
@task_prerun.connect
def task_prerun_handler(sender, task_id, **kwargs):
    print (f"Task {sender} with ID {task_id} is about to start.")
    logger.info(f"Task {sender} with ID {task_id} is about to start.")

@shared_task(
    name="app.tasks.otp_task.send_otp_task",
    max_retries=5,
    default_retry_delay=5,
    acks_late=True,
)
def send_otp_task(phone_no: str, name: str, otp: str):
    try:
        # Initialize WebSocketHandler once
        websocket_handler = WebSocketHandler()

        # WebSocket: Notify the client that the task is in queue
        websocket_handler.send_task_status(phone_no, "queued")

        # Prepare OTP message body
        body = f"""
        Dear {name},
        Your One-Time Password (OTP) is: {otp}
        """
        sms_config = config.sms_api
        auth = (sms_config["SID"], sms_config["AUTH_TOKEN"])

        payload = {
            "Body": body,
            "From": sms_config["PHONE_NUMBER"],
            "To": phone_no,
        }
        twilio_api_url = f"https://api.twilio.com/2010-04-01/Accounts/{sms_config['SID']}/Messages.json"

        # WebSocket: Notify the client that the task is being processed
        websocket_handler.send_task_status(phone_no, "processing")

        # Make the request to Twilio API
        response = requests.post(twilio_api_url, data=payload, auth=auth)
        response.raise_for_status()

        # Check response status
        if response.status_code in [200, 201]:
            # WebSocket: Notify the client that the OTP was sent successfully
            websocket_handler.send_otp(phone_no, otp)
            websocket_handler.send_task_status(phone_no, "success")

            return {"status": "success", "message": "OTP sent successfully"}
        else:
            raise Exception(f"Failed to send OTP: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Twilio API error: {str(e)}")
        websocket_handler.send_task_status(phone_no, "retrying")  # Notify the client retry is happening
        raise send_otp_task.retry(exc=e)  # Retry the task

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        websocket_handler.send_task_status(phone_no, "retrying")  # Notify the client retry is happening
        raise send_otp_task.retry(exc=e)  # Retry the task
