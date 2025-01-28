#  app/curd_operation/sms_curd.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models import SMS
from app.schemas.schema import SMSCreate
from uuid import uuid4

# Create a new SMS entry
async def create_sms(db: AsyncSession, sms: SMSCreate):
    db_sms = SMS(
        uuid=str(uuid4()),  # Generate a new UUID for the SMS
        user_uuid=sms.user_uuid,  # The user associated with the SMS
        payment_uuid=sms.payment_uuid,  # The payment related to the SMS
        qr_code_uuid=sms.qr_code_uuid,  # The QR code related to the SMS
        mobile_no=sms.mobile_no,  # Mobile number for the SMS
        message=sms.message,  # The message content
        message_send_confirmation=sms.message_send_confirmation  # Status of SMS sending
    )
    db.add(db_sms)
    await db.commit()
    await db.refresh(db_sms)
    return db_sms

# Get SMS by UUID
async def get_sms_by_uuid(db: AsyncSession, user_uuid: str):
    result = await db.execute(select(SMS).filter(SMS.user_uuid == user_uuid))
    return result.scalars().first()

# Get all SMS entries (Optional: filter by user, payment, or qr_code if needed)
async def get_all_sms(db: AsyncSession):
    result = await db.execute(select(SMS))
    return result.scalars().all()

# Update SMS details by UUID
async def update_sms(db: AsyncSession, user_uuid: str, sms_data: SMSCreate):
    sms = await get_sms_by_uuid(db, user_uuid)
    if sms:
        sms.mobile_no = sms_data.mobile_no  # Update mobile number
        sms.message = sms_data.message  # Update message content
        sms.message_send_confirmation = sms_data.message_send_confirmation  # Update status
        await db.commit()
        await db.refresh(sms)
        return sms
    return None

#  Delete SMS entry by UUID
async def delete_sms(db: AsyncSession, user_uuid: str):
    sms = await get_sms_by_uuid(db, user_uuid)
    if sms:
        await db.delete(sms)
        await db.commit()
        return sms
    return None
