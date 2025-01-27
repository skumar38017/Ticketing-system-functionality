# app/tasks/otp_task.py
from app.workers.celery_app import celery_app
from app.services.otp_service import send_otp
from app.services.message_service import send_sms

@celery_app.task
def send_otp_task(mobile_no: str, ticket_price: float, ticket_name: str, ticket_qty: int):
    """
    Generates and sends an OTP for ticket booking.
    
    Args:
        mobile_no (str): The mobile number where the OTP will be sent.
        ticket_price (float): The price of the ticket.
        ticket_name (str): The name of the ticket.
        ticket_qty (int): The quantity of tickets.
    """
    otp = send_otp(mobile_no, ticket_price, ticket_name, ticket_qty)
    send_sms(mobile_no, f"mobile_no, ticket_price, ticket_name, ticket_qty")

    return {"message": "OTP sent"}
