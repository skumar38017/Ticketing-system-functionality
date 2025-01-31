# app/services/otp_service.py

import requests
import json
import logging
from app.config import config
from app.utils.generate_otp import generate_otp
from app.database.redisclient import redis_client
from app.tasks.otp_task import send_otp_task
from celery.result import AsyncResult


class OTPService:
    def __init__(self):
        self.logger = logging.getLogger("uvicorn.error")
        self.redis_client = redis_client

    def send_otp(self, phone_no: str, name: str) -> str:
        """
        Publishes OTP task to RabbitMQ queue to be processed asynchronously.

        Args:
            phone_no (str): The phone number.
            name (str): The name associated with the ticket or purpose.

        Returns:
            str: The task ID as a string.
        """
        try:
            # Generate the OTP
            self.logger.info(f"Generating OTP for phone number: {phone_no}, name: {name}")
            otp = generate_otp()
            self.logger.info(f"Generated OTP for phone number: {phone_no}, name: {name}, OTP: {otp}")

            # Publish OTP task to RabbitMQ
            task = send_otp_task.delay(phone_no, name, otp)  # Returns an AsyncResult object
            task_id = task.id  # Extract the task ID as a string
            self.logger.info(f"Task ID {task_id} queued for phone {phone_no} with OTP {otp}")
            return task_id  # Return the task ID as a string

        except Exception as e:
            self.logger.error(f"Error generating OTP: {str(e)}")
            raise e