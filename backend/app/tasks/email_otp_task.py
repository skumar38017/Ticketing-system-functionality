# backend/app/tasks/email_otp_task.py

import logging
import asyncio
from fastapi import HTTPException
from app.config import config
from app.services.websocket_service import WebSocketHandler
from app.utils import validate_email

# Initialize logger
logger = logging.getLogger("email_otp_task")

# Initialize Email Client (Example: SMTP or SendGrid)
# Assuming SendGrid is used for this example. Replace with your email sending logic.
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Initialize WebSocketHandler
websocket_handler = WebSocketHandler()

async def send_email_otp_task(email: str, name: str, otp: str, task_id: str = None, is_retry: bool = False):
    try:
        # Validate input parameters
        if email is None or otp is None or task_id is None:
            raise ValueError("email, otp, and task_id must be provided.")
        
        # Validate and normalize email address
        normalized_email = validate_email(email)
        logger.info(f"Received Email OTP task for {normalized_email} (Retry: {is_retry})")

        # WebSocket: Notify client that the task is queued
        await websocket_handler.send_task_status(normalized_email, "queued")

        # Prepare OTP email body
        body = f"Dear {name}, Your One-Time Password (OTP) is: {otp}"

        # Send OTP asynchronously via SendGrid or any other email service
        response = await send_email_message_async(normalized_email, body)

        # WebSocket: Notify client that the task is processing
        await websocket_handler.send_task_status(normalized_email, "processing")

        # Check the response and notify the client of success/failure
        if response.status_code == 202:
            await websocket_handler.send_task_status(normalized_email, "success")
            logger.info(f"OTP sent successfully to {normalized_email}")
            return {"status": "success", "message": "OTP sent successfully"}
        else:
            await websocket_handler.send_task_status(normalized_email, "retrying")
            raise Exception(f"Failed to send OTP: {response.status_code}")

    except ValueError as ve:
        logger.error(f"Error: {str(ve)}")
        await websocket_handler.send_task_status(normalized_email, "failed")
        raise HTTPException(status_code=400, detail="Invalid input parameters.")
    except Exception as e:
        logger.error(f"Error sending OTP to {normalized_email}: {str(e)}")
        await websocket_handler.send_task_status(normalized_email, "failed")
        raise HTTPException(status_code=500, detail="Failed to send OTP.")

async def send_email_message_async(email: str, body: str):
    try:
        # Simulate Email sending using SendGrid or any other service
        message = Mail(
            from_email='kumar.sumit74604@gmail.com',
            to_emails=email,
            subject="Your OTP",
            plain_text_content=body
        )
        sg = SendGridAPIClient(config.sendgrid_api_key)
        response = await asyncio.to_thread(sg.send, message)
        return response
    except Exception as e:
        logger.error(f"Error sending email to {email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to send email OTP.")
