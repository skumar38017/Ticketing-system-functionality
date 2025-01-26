#  app/schemas/webhook_schema.py

from pydantic import BaseModel

class WebhookBase(BaseModel):
    event: str  # Event type
    data: dict  # Event data
    signature: str  # Signature
    timestamp: str  # Timestamp
    nonce: str  # Nonce
    
class WebhookCreate(WebhookBase):
    pass

class WebhookResponse(WebhookBase): 
    pass    