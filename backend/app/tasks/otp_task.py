# app/tasks/otp_task.py
import logging
import boto3
import asyncio
from fastapi import HTTPException
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

async def send_sns_message_async(phone_no, body):
    try:
        logger.debug(f"Preparing to send OTP to {phone_no} with message: {body}")
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            sns.publish,    
            {'PhoneNumber': normalized_phone_no, 'Message': body}
        )
        logger.debug(f"Response from SNS: {response}")
        return response
    except Exception as e:
        logger.error(f"Failed to send OTP to {phone_no}: {str(e)}")
        return None

# Update send_otp_task to properly await async methods
async def send_otp_task(phone_no: str, name: str, otp: str, task_id: str = None, is_retry: bool = False):
    try:
        # Validate input parameters
        if phone_no is None or otp is None or task_id is None:
            raise ValueError("phone_no, otp, and task_id must be provided.")
        
        # Validate and normalize phone number
        normalized_phone_no = validate_phone(phone_no)
        logger.info(f"Received OTP task for {normalized_phone_no} (Retry: {is_retry})")

        # WebSocket: Notify client that the task is queued
        await websocket_handler.send_task_status(normalized_phone_no, "queued")

        # Prepare OTP message body
        body = f"Dear {name}, Your One-Time Password (OTP) is: {otp}"

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

    except ValueError as ve:
        logger.error(f"Error: {str(ve)}")
        await websocket_handler.send_task_status(normalized_phone_no, "failed")
        raise HTTPException(status_code=400, detail="Invalid input parameters.")
    except Exception as e:
        logger.error(f"Error sending OTP to {normalized_phone_no}: {str(e)}")
        await websocket_handler.send_task_status(normalized_phone_no, "failed")
        raise HTTPException(status_code=500, detail="Failed to send OTP.")