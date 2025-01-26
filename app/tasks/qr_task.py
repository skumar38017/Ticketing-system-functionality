#  app/tasks/qr_task.py

from app.workers.celery_app import celery_app
from app.utils.qr_generator import generate_qr_code
from app.routes.websocket_routes import connected_clients

@celery_app.task
def generate_qr_task(data: dict):
    qr_code = generate_qr_code(data)
    # Notify WebSocket clients
    for client in connected_clients:
        client.send_text("QR code generated successfully!")
    return {"message": "QR code generated"}
