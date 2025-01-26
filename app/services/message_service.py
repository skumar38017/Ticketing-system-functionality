#  app/utils/message_service.py

import requests
from app.config import settings

def send_sms(mobile_no: str, message: str):
    response = requests.post(
        settings.SMS_API_URL,
        json={"mobile": mobile_no, "message": message, "api_key": settings.SMS_API_KEY}
    )
    return response.json()
