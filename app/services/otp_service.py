#  app/services/otp_service.py

import requests
import random
from app.config import config
from app.schemas.schema import SMSCreate
from app.database.models import SMS
from app.database import SessionLocal
from app.utils.generate_otp import generate_otp
def send_otp(mobile_no: str, ticket_price: float, ticket_name: str, ticket_qty: int):
    """
    Sends an OTP for ticket booking with additional details.

    Args:
        mobile_no (str): The mobile number.
        ticket_price (float): The ticket price.
        ticket_name (str): The ticket name.
        ticket_qty (int): The ticket quantity.

    Returns:
        str: The generated OTP.
    """

    otp = generate_otp()

    # Construct the SMS message
    message = f"""
    Your OTP for ticket booking is: {otp}.

    Ticket Details:
    * Ticket Name: {ticket_name}
    * Ticket Price: ₹{ticket_price:.2f}
    * Ticket Quantity: {ticket_qty}

    Valid for 5 minutes.
    """

    # Send the SMS using the SMS API
    response = requests.post(
        config.SMS_API_URL,
        json={
            "mobile": mobile_no,
            "message": message,
            "api_key": config.SMS_API_KEY
        }
    )

    # Store the OTP-related SMS in the database
    db = SessionLocal()
    sms_data = SMSCreate(
        user_id="temporary-user-id",  # This would typically come from the user data
        mobile_no=mobile_no,
        message=message
    )
    db_sms = SMS(**sms_data.dict())
    db.add(db_sms)
    db.commit()
    db.refresh(db_sms)

    # Check API response
    if response.status_code == 200:
        return otp
    else:
        raise Exception(f"Failed to send OTP: {response.text}")
