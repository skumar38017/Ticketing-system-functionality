#  app/services/qr_service.py

from app.config import config
from app.database.redisclient import RedisClient
from app.utils.qr_generator import generate_qr_code
from app.schemas import QRCodeCreate
from app.database.models import QRCode
from app.database import SessionLocal

redis_client = RedisClient()

def generate_qr(data: dict) -> str:
    """
    Generates a QR code and stores it in Redis.

    Args:
        data (dict): The data to encode into the QR code.

    Returns:
        str: The generated QR code.
    """
    # Generate QR code
    qr_code = generate_qr_code(data)

    # Store QR code in Redis
    redis_client.execute_command("SET", "qr_code", qr_code)

    # Store QR code details in the database
    db = SessionLocal()
    qr_data = QRCodeCreate(
        user_id="temporary-user-id",  # This would typically come from user data
        qr_code=qr_code,
        qr_unique_id="unique-id"
    )
    db_qr = QRCode(**qr_data.dict())
    db.add(db_qr)
    db.commit()
    db.refresh(db_qr)

    return qr_code
