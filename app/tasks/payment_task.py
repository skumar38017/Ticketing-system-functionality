# app/tasks/payment_task.py

from app.workers.celery_app import celery_app
from app.services.payment_service import process_payment
import logging

# Set up logger
logger = logging.getLogger("celery.task")  # Use a dedicated logger for Celery tasks

@celery_app.task(name="app.tasks.payment_task.process_payment_task", bind=True)
def process_payment_task(self, payment_data: dict):
    """
    Processes the payment in the background.

    Args:
        payment_data (dict): The data associated with the payment.

    Returns:
        dict: The result of the payment processing.
    """
    try:
        # Process the payment
        result = process_payment(payment_data)
        logger.info(f"Payment processed successfully: {result}")
        return result

    except Exception as e:
        logger.error(f"Error processing payment: {str(e)}")
        self.retry(exc=e, countdown=60)  # Retry the task after 60 seconds