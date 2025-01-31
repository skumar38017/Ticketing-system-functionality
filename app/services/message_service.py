#  app/services/message_service.py

import requests
from app.config import config
from datetime import datetime
from app.database.models import SMS
from app.schemas.schema import UserResponse
from app.schemas.schema import PaymentResponse
from app.schemas.schema import SMSCreate
from app.database import SessionLocal

def send_sms_confirmation(user: dict, payment: dict):
    """
    Sends an SMS confirmation message with booking details.

    Args:
        user (dict): User data containing name and mobile number.
        payment (dict): Payment data containing transaction ID, unique code,
                         ticket generation time, and payment time.

    Returns:
        dict: The response from the SMS API (if SMS is sent).
    """

    message = f"""
    Subject: Your Ticket Booking Confirmation

    Dear {user['name']},

    Thank you for booking your ticket!

    Here are your booking details:

    * Ticket Name: {payment.get('ticket_name', 'N/A')}
    * Transaction ID: {payment['transaction_id']}
    * Unique Code: {payment['unique_code']}
    * Ticket Generated At: {payment['ticket_generated_at'].strftime('%Y-%m-%d %H:%M:%S')}
    * Payment Time: {payment['payment_time'].strftime('%Y-%m-%d %H:%M:%S')}

    Please present this unique code at the counter for verification.

    For any inquiries, please contact us at {config.CONTACT_NUMBER} or {config.CONTACT_EMAIL}.

    Thank you for choosing us.

    Sincerely,

    {config.COMPANY_NAME}
    """

    if user.get('mobile_no'):  # Check if mobile number is available
        response = requests.post(
            config.SMS_API_URL,
            json={
                "mobile": user['mobile_no'],
                "message": message,
                "api_key": config.SMS_API_KEY
            }
        )

        # Create an SMS record in the database
        db = SessionLocal()
        sms_data = SMSCreate(
            user_id=user['uuid'],
            mobile_no=user['mobile_no'],
            message=message
        )
        db_sms = SMS(**sms_data.dict())
        db.add(db_sms)
        db.commit()
        db.refresh(db_sms)

        return response.json()

    else:
        print("Mobile number not found in user data. SMS not sent.")
        return None  # Indicate SMS not sent
