# app/services/otp_service.py

import requests
import json
import logging
from app.config import config
from app.utils.generate_otp import generate_otp
from app.database.redisclient import redis_client
from app.tasks.otp_task import send_otp_task


class OTPService:
    def __init__(self):  # Default to OTPTask if no argument is passed
        self.logger = logging.getLogger("uvicorn.error")
        self.redis_client = redis_client  # Use the existing RedisClient instance

    def send_otp(self, phone_no: str, name: str) -> str:
        """
        Publishes OTP task to RabbitMQ queue to be processed asynchronously.

        Args:
            phone_no (str): The phone number.
            name (str): The name associated with the ticket or purpose.

        Returns:
            str: The OTP that will be processed.
        """       
        try:
            # Generate the OTP
            self.logger.info(f"Generating OTP for phone number: {phone_no}, name: {name}")
            otp = generate_otp()  # Use the utility function to generate OTP
            self.logger.info(f"Generated OTP for phone number: {phone_no}, name: {name}, OTP: {otp}")

            print(f"{name, phone_no}: {otp}")
            # Publish OTP task to RabbitMQ
            send_otp_task.delay(phone_no, name, otp)  # Use .delay() for Celery tasks
            print(self.otp_task)
            return otp

        except Exception as e:
            self.logger.error(f"Error generating OTP: {str(e)}")
            raise e