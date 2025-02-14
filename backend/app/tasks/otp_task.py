# app/tasks/otp_task.py
import logging
import boto3
import asyncio
from app.config import config
from app.services.websocket_service import WebSocketHandler
from app.utils.validator import validate_phone

# Initialize logger
logger = logging.getLogger("otp_task")

# Initialize SNS Client
sns = boto3.client(
    'sns',
    aws_access_key_id=config.aws_credentials["aws_access_key_id"],
    aws_secret_access_key=config.aws_credentials["aws_secret_access_key"],
    region_name=config.aws_credentials["aws_region"],
)

# Initialize WebSocketHandler
websocket_handler = WebSocketHandler()

# Blocking SNS call
def send_sns_message(phone_no, body):
    # Call SNS to send the OTP
    sns.publish(PhoneNumber=phone_no, Message=body)

# Async wrapper for blocking SNS call
# Fully async SNS call
async def send_sns_message_async(phone_no, body):
    try:
        # Asynchronous SNS send logic (SNS itself does not support async, so we're wrapping it with an async method)
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            sns.publish,
            PhoneNumber=phone_no,
            Message=body
        )
        return response
    except Exception as e:
        logger.error(f"Failed to send OTP to {phone_no}: {str(e)}")
        return None


# Update send_otp_task to properly await async methods
async def send_otp_task(phone_no: str, name: str, otp: str, task_id: str = None, body: str = None, properties_value: str = None):
    try:
        # Validate and normalize phone number
        normalized_phone_no = validate_phone(phone_no)
        logger.info(f"Received OTP task for {normalized_phone_no}")

        # WebSocket: Notify client that the task is queued
        await websocket_handler.send_task_status(normalized_phone_no, "queued")

        # Prepare OTP message body
        body = body or f"Dear {name}, Your One-Time Password (OTP) is: {otp}"

        # Send OTP asynchronously to SNS
        response = await send_sns_message_async(normalized_phone_no, body)

        # WebSocket: Notify client that the task is processing
        await websocket_handler.send_task_status(normalized_phone_no, "processing")

        # Check the response and notify the client of success/failure
        if response and response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
            await websocket_handler.send_task_status(normalized_phone_no, "success")
            logger.info(f"OTP sent successfully to {normalized_phone_no}")
            await websocket_handler.send_otp(normalized_phone_no, otp)
            return {"status": "success", "message": "OTP sent successfully"}
        else:
            await websocket_handler.send_task_status(normalized_phone_no, "retrying")
            raise Exception(f"Failed to send OTP: {response.get('ResponseMetadata', {}).get('HTTPStatusCode')}")

    except Exception as e:
        logger.error(f"Error sending OTP to {normalized_phone_no}: {str(e)}")
        await websocket_handler.send_task_status(normalized_phone_no, "failed")
        raise