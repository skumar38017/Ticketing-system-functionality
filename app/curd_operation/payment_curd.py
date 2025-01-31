#  app/curd_operation/payment_curd.py

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Payment
from app.schemas import PaymentCreate, PaymentResponse
from sqlalchemy.exc import SQLAlchemyError

# Create a new payment
async def create_payment(db: AsyncSession, payment: PaymentCreate) -> PaymentResponse:
    try:
        db_payment = Payment(
            user_id=payment.user_id,
            ticket_type=payment.ticket_type,
            ticket_price=payment.ticket_price,
            ticket_qty=payment.ticket_qty,
            payment_method=payment.payment_method,
            transaction_id=payment.transaction_id,
            transaction_status=payment.transaction_status,
            transaction_fee=payment.transaction_fee,
            amount=payment.amount,
            status=payment.status,
            gst=payment.gst,
            i_gst=payment.i_gst,
            s_gst=payment.s_gst,
            c_gst=payment.c_gst
        )
        db.add(db_payment)
        await db.commit()
        await db.refresh(db_payment)
        return PaymentResponse.from_orm(db_payment)
    except SQLAlchemyError as e:
        await db.rollback()
        raise e

# Get a payment by UUID
async def get_payment_by_uuid(db: AsyncSession, uuid: str) -> PaymentResponse:
    try:
        query = select(Payment).filter(Payment.uuid == uuid)
        result = await db.execute(query)
        payment = result.scalars().first()
        if payment:
            return PaymentResponse.from_orm(payment)
        return None
    except SQLAlchemyError as e:
        raise e

# Update payment information
async def update_payment(db: AsyncSession, uuid: str, payment: PaymentCreate) -> PaymentResponse:
    try:
        query = select(Payment).filter(Payment.uuid == uuid)
        result = await db.execute(query)
        db_payment = result.scalars().first()
        if db_payment:
            db_payment.ticket_type = payment.ticket_type
            db_payment.ticket_price = payment.ticket_price
            db_payment.ticket_qty = payment.ticket_qty
            db_payment.payment_method = payment.payment_method
            db_payment.transaction_id = payment.transaction_id
            db_payment.transaction_status = payment.transaction_status
            db_payment.transaction_fee = payment.transaction_fee
            db_payment.amount = payment.amount
            db_payment.status = payment.status
            db_payment.gst = payment.gst
            db_payment.i_gst = payment.i_gst
            db_payment.s_gst = payment.s_gst
            db_payment.c_gst = payment.c_gst
            await db.commit()
            await db.refresh(db_payment)
            return PaymentResponse.from_orm(db_payment)
        return None
    except SQLAlchemyError as e:
        await db.rollback()
        raise e

# Delete a payment by UUID
async def delete_payment(db: AsyncSession, uuid: str) -> bool:
    try:
        query = select(Payment).filter(Payment.uuid == uuid)
        result = await db.execute(query)
        db_payment = result.scalars().first()
        if db_payment:
            await db.delete(db_payment)
            await db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        await db.rollback()
        raise e
