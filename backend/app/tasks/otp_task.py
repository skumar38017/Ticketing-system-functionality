# app/tasks/otp_task.py
from celery import shared_task
import logging
import requests
import boto3
from app.config import config
from celery.signals import task_prerun
from celery.exceptions import MaxRetriesExceededError
from app.services.websocket_service import WebSocketHandler

# Initialize logger
logger = logging.getLogger("celery.task")

# Initialize SNS Client
sns = boto3.client(
    'sns',
    aws_access_key_id=config.aws_credentials["aws_access_key_id"],
    aws_secret_access_key=config.aws_credentials["aws_secret_access_key"],
    region_name=config.aws_credentials["region"]
)

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

        # SNS: Publish OTP message to the SNS Topic
        response = sns.publish(
            PhoneNumber=phone_no,  # Send message to this phone number
            Message=body  # Message body containing OTP
        )

        # WebSocket: Notify the client that the task is being processed
        websocket_handler.send_task_status(phone_no, "processing")

        # Check if the message was successfully sent via SNS
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            # WebSocket: Notify the client that the OTP was sent successfully
            websocket_handler.send_otp(phone_no, otp)
            websocket_handler.send_task_status(phone_no, "success")

            return {"status": "success", "message": "OTP sent successfully"}
        else:
            raise Exception(f"Failed to send OTP: {response['ResponseMetadata']['HTTPStatusCode']}")
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        websocket_handler.send_task_status(phone_no, "retrying")  # Notify the client retry is happening
        raise send_otp_task.retry(exc=e)  # Retry the task
