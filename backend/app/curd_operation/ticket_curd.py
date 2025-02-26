#  app/curd_operation/ticket_curd.py

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Payment
from app.schemas import PaymentCreate, PaymentResponse
from sqlalchemy.exc import SQLAlchemyError
from fastapi import  HTTPException
import logging

logger = logging.getLogger("uvicorn.error")

async def create_payment(db: AsyncSession, payment: PaymentCreate) -> PaymentResponse:
    """
    Create a new payment in the database.
    """
    try:
        db_payment = Payment(
            user_uuid=payment.user_uuid,  # Ensure this matches the field in your schema/model
            ticket_description=payment.ticket_description,
            ticket_type=payment.ticket_type,
            ticket_price=payment.ticket_price,
            ticket_qty=payment.ticket_qty,
            payment_method=payment.payment_method,
            transaction_id=payment.transaction_id,
            transaction_status=payment.transaction_status,
            transaction_fee=payment.transaction_fee,
            total_amount=payment.total_amount,
            gst=payment.gst,
            i_gst=payment.i_gst,
            s_gst=payment.s_gst,
            c_gst=payment.c_gst,
        )

        db.add(db_payment)
        await db.commit()
        await db.refresh(db_payment)
        logger.info(f"Created payment with transaction ID: {payment.transaction_id}")
        return PaymentResponse.from_orm(db_payment)
    except SQLAlchemyError as e:
        logger.error(f"Failed to create payment: {str(e)}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred creating the payment")

async def get_payment_by_uuid(db: AsyncSession, uuid: str) -> PaymentResponse:
    """
    Retrieve a payment by its UUID.
    """
    try:
        query = select(Payment).filter(Payment.uuid == uuid)
        result = await db.execute(query)
        payment = result.scalars().first()
        if payment:
            return PaymentResponse.from_orm(payment)
        return None
    except SQLAlchemyError as e:
        logger.error(f"Failed to retrieve payment with UUID {uuid}: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred retrieving the payment")

async def update_payment(db: AsyncSession, uuid: str, payment_data: PaymentCreate) -> PaymentResponse:
    """
    Update an existing payment in the database.
    """
    try:
        query = select(Payment).filter(Payment.uuid == uuid)
        result = await db.execute(query)
        db_payment = result.scalars().first()

        if db_payment:
            db_payment.ticket_description = payment_data.ticket_description
            db_payment.ticket_type = payment_data.ticket_type
            db_payment.ticket_price = payment_data.ticket_price
            db_payment.ticket_qty = payment_data.ticket_qty
            db_payment.payment_method = payment_data.payment_method
            db_payment.transaction_id = payment_data.transaction_id
            db_payment.transaction_status = payment_data.transaction_status
            db_payment.transaction_fee = payment_data.transaction_fee
            db_payment.total_amount = payment_data.total_amount
            db_payment.gst = payment_data.gst
            db_payment.i_gst = payment_data.i_gst
            db_payment.s_gst = payment_data.s_gst
            db_payment.c_gst = payment_data.c_gst

            await db.commit()
            await db.refresh(db_payment)

            logger.info(f"Updated payment with UUID {uuid}")
            return PaymentResponse.from_orm(db_payment)
        return None
    except SQLAlchemyError as e:
        logger.error(f"Failed to update payment with UUID {uuid}: {str(e)}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred updating the payment")

async def delete_payment(db: AsyncSession, uuid: str) -> bool:
    """
    Delete a payment from the database by its UUID.
    """
    try:
        query = select(Payment).filter(Payment.uuid == uuid)
        result = await db.execute(query)
        db_payment = result.scalars().first()

        if db_payment:
            await db.delete(db_payment)
            await db.commit()
            logger.info(f"Deleted payment with UUID {uuid}")
            return True
        else:
            logger.warning(f"Payment with UUID {uuid} not found for deletion")
            return False
    except SQLAlchemyError as e:
        logger.error(f"Failed to delete payment with UUID {uuid}: {str(e)}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred deleting the payment")