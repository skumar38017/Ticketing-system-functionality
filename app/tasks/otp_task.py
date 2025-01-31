# app/tasks/otp_task.py
from celery import shared_task
import logging
import requests
from app.config import config
from app.services.websocket_service import WebSocketHandler

@shared_task(name="app.tasks.otp_task.send_otp_task")
def send_otp_task(phone_no: str, name: str, otp: str):
    logger = logging.getLogger("celery.task")  # Use a dedicated logger for Celery tasks

    """
    Function to send OTP via Twilio, registered as a Celery task.
    """
    try:
        # Log input data for debugging
        logger.debug(f"Received OTP request: phone_no={phone_no}, name={name}, otp={otp}")

        # Compose the SMS message
        body = f"""
        Dear {name},

        Your One-Time Password (OTP) is: {otp}
        Please enter this code on the verification page to complete your request. 
        This OTP is valid for the next 5 minutes.
        If you did not request this OTP, please ignore this message.

        Thank you,
        OTP Testing Team
        """

        # Log the message body for debugging
        logger.debug(f"Message body prepared: {body}")

        # Twilio SMS API configuration
        sms_config = config.sms_api
        auth = (sms_config["SID"], sms_config["AUTH_TOKEN"])  # Basic Auth

        # Prepare request payload
        payload = {
            "Body": body,
            "From": sms_config["PHONE_NUMBER"],  # Your Twilio number
            "To": phone_no,  # Recipient's phone number
        }
        logger.debug(f"Twilio payload: {payload}")

        # Twilio API endpoint
        twilio_api_url = "https://api.twilio.com/2010-04-01/Accounts/{SID}/Messages.json".format(SID=sms_config["SID"])

        # Make POST request to Twilio
        response = requests.post(twilio_api_url, data=payload, auth=auth)
        logger.debug(f"Twilio response: {response.status_code} - {response.text}")
        response.raise_for_status()

        # Check response
        if response.status_code in [200, 201]:  # Twilio returns 201/200 for success
            logger.info(f"OTP sent successfully to {phone_no}")
            WebSocketHandler().send_otp(phone_no, otp)  # Notify via WebSocket if applicable
            return {"status": "success", "message": "OTP sent successfully"}
        else:
            logger.error(f"Failed to send OTP: {response.status_code} - {response.text}")
            raise Exception(f"Failed to send OTP: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Twilio API error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise
    
# from app.workers.celery_app import celery_app
# from app.services.websocket_service import WebSocketHandler
# import asyncio
# import requests
# from app.config import config
# import logging

# logger = logging.getLogger("uvicorn.error")

# @celery_app.task(name="app.tasks.otp_task.send_otp_task")
# def send_otp_task(phone_no: str, name: str, otp: str):
#     """
#     Celery task to generate and send OTP.

#     Args:
#         phone_no (str): The phone number to send the OTP.
#         name (str): The name associated with the OTP.
#         otp (str): The OTP to send.
#     """
#     try:
#         message = f"""
#         Your OTP for processing Neon-Stdio-Holi-T25 is {otp}
        
#         Ticket Details:
#         * Name: {name}

#         Valid for 5 minutes.
#         """

#         response = requests.post(
#             config.SMS_API_URL,
#             json={
#                 "mobile": phone_no,
#                 "message": message,
#                 "api_key": config.SMS_API_KEY,
#             },
#         )

#         if response.status_code == 200:
#             logger.info(f"OTP sent successfully to {phone_no}")
#             asyncio.run(WebSocketHandler().send_otp(phone_no, otp))
#         else:
#             raise Exception(f"Failed to send OTP: {response.text}")
    
#     except Exception as e:
#         logger.error(f"Error sending OTP: {str(e)}")
#         raise e