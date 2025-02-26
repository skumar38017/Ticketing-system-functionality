#  app/routes/ticket_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schema import TicketChoice, PaymentCreate, PaymentResponse
from app.utils.razorpay_utils import RazorpayClient
from app.database.database import get_db
from app.curd_operation.ticket_curd import create_payment
from app.services.websocket_service import WebSocketHandler
import logging

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()
ws_handler = WebSocketHandler()

@router.post("/choose-ticket/", response_model=PaymentResponse)
async def choose_ticket(
    user_uuid: str,
    ticket_choice: TicketChoice, 
    db: AsyncSession = Depends(get_db)
):
    try:
        # Calculate total amount
        total_amount = ticket_choice.ticket_price * ticket_choice.ticket_qty

        # Prepare payment data
        payment_data = {
            "amount": total_amount * 100,  # Convert to paise
            "currency": "INR",
            "payment_capture": 1,  # Auto capture payment after success
        }

        # Create Razorpay order
        razorpay_response = RazorpayClient.create_order(payment_data, user_uuid=user_uuid, payment_method=ticket_choice.payment_method)
        
        if not razorpay_response or "id" not in razorpay_response:
            raise HTTPException(status_code=400, detail="Unable to create order")

        # Create a payment record in the database
        payment_create = PaymentCreate(
            user_id=user_uuid,  # Using the user_uuid passed to this endpoint
            ticket_description=ticket_choice.ticket_description,
            ticket_type=ticket_choice.ticket_type,
            ticket_price=ticket_choice.ticket_price,
            ticket_qty=ticket_choice.ticket_qty,
            payment_method=ticket_choice.payment_method,
            transaction_id=razorpay_response["id"],  # Transaction ID from Razorpay response
            transaction_fee=0,
            total_amount=total_amount,
            transaction_status="due"
        )

        # Save payment details in the database
        new_payment = await create_payment(db, payment_create)
        
        # Notify using WebSocket about the order creation
        await ws_handler.broadcast(f"Order with transaction ID {payment_create.transaction_id} created for user {user_uuid}")

        return new_payment
    
    except Exception as e:
        logger.exception(f"❌ Error during ticket purchase: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during ticket purchase")