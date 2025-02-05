# app/services/otp_service.py
import logging
import asyncio  # Import asyncio for async operations
from app.utils.generate_otp import generate_otp
from app.tasks.otp_task import send_otp_task
from celery.result import AsyncResult
from app.database.redisclient import redis_client
from app.services.websocket_service import WebSocketHandler
from app.config import config
import time
from fastapi import HTTPException


class OTPService:
    def __init__(self):
        self.logger = logging.getLogger("uvicorn.error")
        self.redis_client = redis_client
        self.websocket_handler = WebSocketHandler()

    async def send_otp(self, phone_no: str, name: str, otp: str) -> str:
        """
        Publishes OTP task to RabbitMQ and tracks its status asynchronously.
        Notifies the client via WebSocket.
        """
        try:
            # Notify client that the task is queued
            await self.websocket_handler.send_task_status(phone_no, "queued")

            # Trigger the OTP task asynchronously
            task_result = send_otp_task.delay(phone_no, name, otp)
            task_id = task_result.id
            self.logger.info(f"OTP task queued with ID {task_id} for phone {phone_no}")

            # Track the task's status
            asyncio.create_task(self._track_task_status(task_id, phone_no))

            return task_id

        except Exception as e:
            self.logger.error(f"Error sending OTP: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to send OTP.")

    async def _track_task_status(self, task_id: str, phone_no: str):
        """
        Tracks the status of a Celery task and notifies the client via WebSocket.
        """
        try:
            task_result = AsyncResult(task_id)

            while task_result.status not in ["SUCCESS", "FAILURE"]:
                self.logger.debug(f"Task {task_id} status: {task_result.status}")
                if task_result.status == "STARTED":
                    await self.websocket_handler.send_task_status(phone_no, "processing")
                await asyncio.sleep(1)
                task_result = AsyncResult(task_id)

            # Final task status
            if task_result.status == "SUCCESS":
                await self.websocket_handler.send_task_status(phone_no, "success")
                self.logger.info(f"Task {task_id} completed successfully.")
            else:
                await self.websocket_handler.send_task_status(phone_no, "failed")
                self.logger.error(f"Task {task_id} failed.")

        except Exception as e:
            self.logger.error(f"Error tracking task {task_id}: {str(e)}")
            await self.websocket_handler.send_task_status(phone_no, "failed")