# app/services/otp_service.py
import logging
import uuid
import asyncio
from fastapi import HTTPException
from app.config import config
from app.services.websocket_service import WebSocketHandler
from app.database.redisclient import redis_client
from app.utils.generate_otp import generate_otp
from app.settings import settings
import aio_pika

class OTPService:
    def __init__(self):
        self.logger = logging.getLogger("uvicorn.error")
        self.redis_client = redis_client
        self.websocket_handler = WebSocketHandler()

    async def send_otp(self, phone_no: str, name: str, otp: str) -> str:
        try:
            # Notify WebSocket that the task is queued
            await self.websocket_handler.send_task_status(phone_no, "queued")

            # Generate a unique task ID
            task_id = str(uuid.uuid4())

            # Initialize retry attempts in Redis
            retry_attempts = int(self.redis_client.get(f"otp_retry_{phone_no}") or 0)
            is_retry = retry_attempts > 0  # Determine if this is a retry

            # Send the OTP task to RabbitMQ asynchronously
            await self._send_otp_to_rabbitmq(phone_no, name, otp, task_id, is_retry=is_retry)

            # Log the task ID
            self.logger.info(f"OTP task queued with ID {task_id} for phone {phone_no}")

            # Track the task status asynchronously
            asyncio.create_task(self._track_task_status(task_id, phone_no, otp))
            return task_id

        except Exception as e:
            self.logger.error(f"Error sending OTP: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to send OTP.")
    
    async def _track_task_status(self, task_id: str, phone_no: str, otp: str):
        """
        Track the status of the OTP task and notify the client via WebSocket.
        """
        attempts = int(self.redis_client.get(f"otp_retry_{phone_no}") or 0)  # Default to 0 if no retries found
        try:
            await asyncio.sleep(2)  # Simulate processing time
            await self.websocket_handler.send_task_status(phone_no, "processing")

            # Retry logic for OTP delivery (up to 3 attempts)
            if attempts < 2:
                if await self._send_otp(phone_no, otp):  # Replace with real OTP delivery logic
                    await self.websocket_handler.send_task_status(phone_no, "success")
                    self.logger.info(f"Task {task_id} completed successfully.")
                else:
                    # Retry sending OTP
                    attempts += 1
                    self.redis_client.setex(f"otp_retry_{phone_no}", attempts, config.otp_expiration_time)
                    await self.websocket_handler.send_task_status(phone_no, f"retrying attempt {attempts}")
                    await self._track_task_status(task_id, phone_no, otp)
            else:
                await self.websocket_handler.send_task_status(phone_no, "failed")
                self.logger.error(f"Task {task_id} failed after 3 attempts.")
        except Exception as e:
            self.logger.error(f"Error tracking task {task_id}: {str(e)}")
            await self.websocket_handler.send_task_status(phone_no, "failed")

    async def _send_otp(self, phone_no: str, otp: str) -> bool:
        """
        Attempt to send OTP and return success or failure.
        """
        try:
            # Simulate OTP sending logic (replace with actual OTP service integration)
            success = True  # Assume OTP was sent successfully
            if not success:
                return False
            return True
        except Exception as e:
            self.logger.error(f"Error sending OTP to {phone_no}: {str(e)}")
            return False

    async def _send_otp_to_rabbitmq(self, phone_no: str, name: str, otp: str, task_id: str, is_retry: bool = False):
        try:
            # Ensure all required values are provided
            if any(x is None for x in [phone_no, name, otp, task_id]):
                raise ValueError("One or more required fields are missing.")
                    
            # Dynamically select which queue to send based on retry flag
            selected_queue = 'otp_queue_2' if is_retry else 'otp_queue_1'
    
            # Prepare the message (include task_id and retry flag for tracking)
            message_body = f"{phone_no}|{name}|{otp}|{task_id}|{int(is_retry)}"
    
            # Connect to RabbitMQ
            connection = await aio_pika.connect_robust(host=settings.RABBITMQ_HOST)
            async with connection:
                # Create a channel
                channel = await connection.channel()
    
                # Declare the OTP queue (ensure it's durable)
                queue = await channel.declare_queue(selected_queue, durable=True)
    
                # Create the message object
                message = aio_pika.Message(
                    body=message_body.encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT  # Ensure message persistence
                )
    
                # Publish the message to the queue
                await channel.default_exchange.publish(
                    message,
                    routing_key=selected_queue
                )
                self.logger.info(f"Sent OTP task to RabbitMQ for phone {phone_no} on queue {selected_queue}")
    
        except ValueError as ve:
            self.logger.error(f"Error: {str(ve)}")
            raise HTTPException(status_code=400, detail="Invalid input values.")
        except Exception as e:
            self.logger.error(f"Error sending OTP task to RabbitMQ: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to send OTP task to RabbitMQ.")