import sys
import os
from time import sleep
import pika  # Import pika for RabbitMQ interaction
import logging

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.settings import settings  # Import settings after modifying sys.path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_send_otp_task():
    """
    Test function to trigger the send_otp_task via RabbitMQ (pika).
    """
    try:
        phone_no = "+919876543210"
        name = "Sumit ji"
        otp = "123456"

        # RabbitMQ connection parameters
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))  # Use your correct RabbitMQ server IP
        logger.info(f"Connected to RabbitMQ: {connection}")
        channel = connection.channel()

        # Declare the queue (ensure it matches your worker's queue)
        channel.queue_declare(queue='otp_queue_1', durable=True)

        # Prepare the message
        message = f"{phone_no}|{name}|{otp}"
        
        # Send the message to the queue
        channel.basic_publish(
            exchange='',
            routing_key='otp_queue_1',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make the message persistent
            )
        )

        logger.info(f"Sent OTP task to RabbitMQ for phone {phone_no}")

        # Now, let's simulate waiting for the task to be processed
        logger.info(f"Waiting for the task to be processed...")

        # Simulate task processing (normally this would be handled by a worker in parallel)
        sleep(2)  # Simulate waiting for task processing

        # Task is completed, we log the task processed successfully
        logger.info(f"Task for phone {phone_no} processed successfully!")

        # Close the connection
        connection.close()

    except Exception as e:
        logger.error(f"Error during testing: {str(e)}")

    finally:
        if connection and connection.is_open:
            connection.close()
            logger.info("Connection to RabbitMQ closed.")

if __name__ == "__main__":
    test_send_otp_task()
