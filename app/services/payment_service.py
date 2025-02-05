#  app/services/payment_service.py

from app.config import config
from app.database.redisclient import RedisClient

redis_client = RedisClient()

def process_payment(payment_data: dict):
    """
    Processes the payment.

    Args:
        payment_data (dict): The payment data (e.g., amount, transaction details).

    Returns:
        str: Payment status message.
    """
    # Simulating payment processing logic
    # You could connect with payment gateways, handle success/fail responses, etc.
    
    # Store the payment status in Redis (for demonstration purposes)
    redis_client.execute_command("SET", "payment_status", "processed")
    
    return "Payment processed successfully"
