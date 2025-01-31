# app/tasks/qr_task.py

from app.workers.celery_app import celery_app
from app.utils.qr_generator import generate_qr_code
from app.services.websocket_service import WebSocketHandler
import logging

# Set up logger
logger = logging.getLogger("celery.task")  # Use a dedicated logger for Celery tasks

@celery_app.task(name="app.tasks.qr_task.generate_qr_task", bind=True)
def generate_qr_task(self, data: dict):
    """
    Generates a QR code and notifies WebSocket clients about the success.

    Args:
        data (dict): The data to encode into the QR code.

    Returns:
        dict: A dictionary containing a success message and the generated QR code data.
    """
    try:
        # Generate the QR code
        qr_code = generate_qr_code(data)

        # Notify all WebSocket clients about the QR code generation
        websocket_handler = WebSocketHandler()
        print(f"Active connections: {websocket_handler.active_connections}")
        for client in websocket_handler.active_connections:
            try:
                print(f"Sending message to client: {client}")
                client.send_text(f"QR code generated successfully!{qr_code}")
            except Exception as ws_error:
                logger.error(f"Failed to notify WebSocket client: {str(ws_error)}")

        # Return success response
        logger.info(f"QR code generated successfully: {qr_code}")
        return {"message": "QR code generated", "ticket": data, "qr_code": qr_code}

    except Exception as e:
        logger.error(f"Error generating QR code: {str(e)}")
        self.retry(exc=e, countdown=60)  # Retry the task after 60 seconds