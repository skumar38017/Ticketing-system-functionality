#  app/curd_operation/qr_code_curd.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models import QRCode
from app.schemas import QRCodeCreate

# Create a new QR code
async def create_qr_code(db: AsyncSession, qr_code: QRCodeCreate):
    db_qr_code = QRCode(
        qr_code=qr_code.qr_code,  # This should be the actual QR code data
        qr_unique_id=qr_code.qr_unique_id,
        user_uuid=qr_code.user_uuid,
        payment_uuid=qr_code.payment_uuid
    )
    db.add(db_qr_code)
    await db.commit()
    await db.refresh(db_qr_code)
    return db_qr_code

# Get a QR code by UUID
async def get_qr_code_by_uuid(db: AsyncSession, uuid: str):
    result = await db.execute(select(QRCode).filter(QRCode.uuid == uuid))
    return result.scalars().first()

# Get all QR codes for a user
async def get_qr_codes_by_user_uuid(db: AsyncSession, user_uuid: str):
    result = await db.execute(select(QRCode).filter(QRCode.user_uuid == user_uuid))
    return result.scalars().all()

# Update QR code details
async def update_qr_code(db: AsyncSession, uuid: str, qr_code_data: QRCodeCreate):
    qr_code = await get_qr_code_by_uuid(db, uuid)
    if qr_code:
        qr_code.qr_code = qr_code_data.qr_code  # Update QR code data
        qr_code.qr_unique_id = qr_code_data.qr_unique_id  # Update unique ID
        qr_code.user_uuid = qr_code_data.user_uuid  # Update user ID
        qr_code.payment_uuid = qr_code_data.payment_uuid  # Update payment UUID
        await db.commit()
        await db.refresh(qr_code)
        return qr_code
    return None

# Delete a QR code by UUID
async def delete_qr_code(db: AsyncSession, uuid: str):
    qr_code = await get_qr_code_by_uuid(db, uuid)
    if qr_code:
        await db.delete(qr_code)
        await db.commit()
        return qr_code
    return None
