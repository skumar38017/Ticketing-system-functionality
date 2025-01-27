# app/tasks/qr_task.py
from app.workers.celery_app import celery_app
from app.utils.qr_generator import generate_qr_code
from app.services.websocket_service import WebSocketHandler

websocket_handler = WebSocketHandler()

@celery_app.task
def generate_qr_task(data: dict):
    """
    Generates a QR code and notifies WebSocket clients about the success.
    
    Args:
        data (dict): The data to encode into the QR code.
    """
    qr_code = generate_qr_code(data)

    # Notify all WebSocket clients about the QR code generation
    for client in websocket_handler.active_connections:
        client.send_text("QR code generated successfully!")

    return {"message": "QR code generated", "ticket": "data, qr_code"}
