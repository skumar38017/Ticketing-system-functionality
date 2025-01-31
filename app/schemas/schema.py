#  app/schemas/user_schema.py

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from app.utils.validator import validate_phone  # Import your custom validator


# User schema
class UserBase(BaseModel):
    name: str = Field(..., max_length=50)
    email: EmailStr
    phone_no: str = Field(..., max_length=16, min_length=10)  # Adjusted for international support
    is_active: Optional[bool] = True  # Default value is set here

    # Use @field_validator in Pydantic V2
    @field_validator("phone_no")
    @classmethod
    def validate_phone_no(cls, value):
        return validate_phone(value)

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    uuid: str
    name: str
    email: str
    phone_no: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  

# Payment Schema
class PaymentBase(BaseModel):
    ticket_description: str = Field(..., max_length=500)
    ticket_type: str = Field(..., max_length=50)
    ticket_price: int
    ticket_qty: int
    payment_method: str = Field(..., max_length=50)
    transaction_id: str = Field(..., max_length=50)
    disscount: float = 0
    transaction_fee: float
    invoice_amount: float = 0
    gst: float = 0
    i_gst: float = 0
    s_gst: float = 0
    c_gst: float = 0
    total_tax: float = 0
    total_amount: float = 0
    transaction_status: str = Field(..., pattern="^(successfully|failed|processing|cancelled|due)$")


class PaymentCreate(PaymentBase):
    user_id: str


class PaymentResponse(PaymentBase):
    uuid: str
    user_id: str
    ticket_description: str
    ticket_type: str
    ticket_price: str
    ticket_qty: str
    payment_method: str
    transaction_id: str
    disscount: float
    transaction_fee: float
    invoice_amount: float
    gst: float
    i_gst: float
    s_gst: float    
    c_gst: float
    total_tax: float
    total_amount: float
    transaction_status: str
    issued_date: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# QR Code schema
class QRCodeBase(BaseModel):
    qr_code: str = Field(..., max_length=50)
    qr_unique_id: str = Field(..., max_length=50)


class QRCodeCreate(QRCodeBase):
    user_id: str
    payment_uuid: str


class QRCodeResponse(QRCodeBase):
    uuid: str
    user_id: str
    payment_uuid: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# SMS schema
class SMSBase(BaseModel):
    mobile_no: str = Field(..., max_length=10, min_length=10)
    message: str = Field(..., max_length=500)
    message_send_confirmation: str = Field(..., pattern="^(successfully|failed)$")


class SMSCreate(SMSBase):
    user_id: str
    payment_uuid: str
    qr_code_uuid: str


class SMSResponse(SMSBase):
    uuid: str
    user_id: str
    payment_uuid: str
    qr_code_uuid: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Email Schema
class EmailBase(BaseModel):
    email: EmailStr
    message: str = Field(..., max_length=50)


class EmailCreate(EmailBase):
    user_id: str


class EmailResponse(EmailBase):
    uuid: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
