#  app/services/qr_service.py

from app.config import config
from app.database.redisclient import RedisClient
from app.utils.qr_generator import generate_qr_code

redis_client = RedisClient()

def generate_qr(data: dict):
    # Generate QR code
    qr_code = generate_qr_code(data)
    # Store QR code in Redis
    redis_client.execute_command("SET", "qr_code", qr_code) 