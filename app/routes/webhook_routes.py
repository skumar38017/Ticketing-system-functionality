#  app/routes/webhook_routes.py

from fastapi import APIRouter, HTTPException, Request

router = APIRouter()

@router.post("/webhook/payment", response_model=schemas.UserResponse)
async def razorpay_webhook(
    request: Request):
    try:
        payload = await request.json()
        # Process the webhook data here
        # Example: payment status update
        if payload.get("event") == "payment.captured":
            # Handle successful payment event
            return {"message": "Payment captured successfully"}
        elif payload.get("event") == "payment.failed":
            # Handle payment failure event
            return {"message": "Payment failed"}
        else:
            return {"message": "Event not handled"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
