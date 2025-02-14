# backend/app/RabbitMQ_Consumer/otp_queue.py

import os
import sys
import pika
import logging
from app.config import config
from app.tasks.otp_task import send_otp_task
from app.settings import settings
import time
import asyncio
import aio_pika

# Fix the sys.path.append() line.
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.getLogger("pika").setLevel(logging.DEBUG)
# print(f"{logging.getLogger('pika').level}")
logger = logging.getLogger(__name__)
# logging.getLogger("pika").addHandler(logging.StreamHandler())

# This callback function processes tasks from the queues
async def callback(message: aio_pika.IncomingMessage):
    try:
        message_body = message.body.decode()
        logging.info(f"Received message: {message_body}")

        # Split by pipe "|" and check the length of the message
        message_parts = message_body.split("|")
        
        # OTP message validation
        if len(message_parts) not in [3, 4, 6]:
            logging.warning(f"Skipping invalid message: {message_body}")
            logging.debug(f"Acknowledging message: {message_body}")
            await message.ack()
            return

        phone_no, name, otp, task_id, body, properties_value = (message_parts + [None] * 3)[:6]
        logging.info(f"Processing OTP for Phone: {phone_no}, Name: {name}, OTP: {otp}, Task ID: {task_id}, Body: {body}, Properties: {properties_value}")

        # Retry logic for OTP delivery
        max_retries = 3
        retry_count = 0
        otp_delivered = False

        while retry_count < max_retries and not otp_delivered:
            retry_count += 1
            logging.info(f"Attempt {retry_count}/{max_retries}: Processing OTP for Phone {phone_no}...")

            otp_delivered = await send_otp_task(phone_no, name, otp, task_id, body, properties_value)

            if otp_delivered:
                logging.info(f"OTP successfully delivered to {phone_no}.")
                logging.debug(f"Acknowledging message: {phone_no}")
                await message.ack()
                return
            else:
                logging.warning(f"OTP delivery attempt {retry_count} failed for {phone_no}. Retrying...")
                time.sleep(2)  # Sleep (Blocking) before retrying

        if not otp_delivered:
            logging.error(f"Failed to deliver OTP to {phone_no} after {max_retries} attempts.")
            logging.debug(f"Acknowledging message: {max_retries}")
            await message.ack()

    except Exception as e:
        logging.error(f"Error processing message: {e}")
        await message.nack(requeue=True)

# Function to dynamically handle queues and bind them
async def start_worker():
    try:
        # Connect to RabbitMQ asynchronously using aio_pika
        connection = await aio_pika.connect_robust(host=settings.RABBITMQ_HOST)
        logging.info(f"Connected to RabbitMQ")

        async with connection:
            channel = await connection.channel()  # Create a new channel

            # Declare OTP Queues dynamically
            queues = ['otp_queue_1', 'otp_queue_2']  # List of queues to process OTP tasks
            exchanges = ['otp_exchange_1', 'otp_exchange_2']

            for queue_name, exchange_name in zip(queues, exchanges):
                # Declare OTP Queue
                queue = await channel.declare_queue(queue_name, durable=True)

                # Declare OTP Exchange
                exchange = await channel.declare_exchange(exchange_name, aio_pika.ExchangeType.DIRECT)

                # Bind the queue to the respective exchange
                await queue.bind(exchange, routing_key=queue_name)

                # Set the callback function to handle messages from OTP queues
                logging.info(f"Consuming from {queue_name}...")
                await queue.consume(callback)  # Use `consume` instead of `basic_consume`

            logging.info("Waiting for OTP messages...")
            # Start consuming from all OTP queues asynchronously
            # Keep the consumer running
            await asyncio.Future()  # Run forever

    except Exception as e:
        logging.error(f"Error while connecting or consuming messages from RabbitMQ: {e}")

if __name__ == "__main__":
    asyncio.run(start_worker())
