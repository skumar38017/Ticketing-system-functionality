# app/tasks/otp_task.py

from app.workers.celery_app import celery_app
from app.services.websocket_service import WebSocketHandler
import asyncio
import requests
from app.config import config
import logging

class OTPTask:
    def __init__(self):
        self.websocket_handler = WebSocketHandler()
        self.logger = logging.getLogger("uvicorn.error")

    @celery_app.task
    def send_otp_task(phone_no: str, name: str, otp: str):
        """
        Celery task to generate and send OTP.

        Args:
            phone_no (str): The phone number to send the OTP.
            name (str): The name associated with the OTP.
            otp (str): The OTP to send.

        """
        try:
            # Construct the SMS message
            message = f"""
            Your OTP for processing Neon-Stdio-Holi-T25 is {otp}
            
            Ticket Details:
            * Name: {name}

            Valid for 5 minutes.
            """

            # Send the SMS using the SMS API
            response = requests.post(
                config.SMS_API_URL,
                json={
                    "mobile": phone_no,
                    "message": message,
                    "api_key": config.SMS_API_KEY,
                },
            )

            # Check SMS API response
            if response.status_code == 200:
                print(f"OTP sent successfully to {phone_no}")
                
                # Notify WebSocket clients about the OTP
                asyncio.run(WebSocketHandler().send_otp(phone_no, otp))
            else:
                raise Exception(f"Failed to send OTP: {response.text}")
        
        except Exception as e:
            print(f"Error sending OTP: {str(e)}")
            raise e