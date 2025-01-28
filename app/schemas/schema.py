#  app/schemas/user_schema.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
import uuid

# User schema
class UserBase(BaseModel):
    name: str = Field(..., max_length=50)
    email: EmailStr
    phone_no: str = Field(..., max_length=10, min_length=10)
    is_active: Optional[bool] = True



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
        orm_mode = True


# Payment Schema
class PaymentBase(BaseModel):
    ticket_type: str = Field(..., max_length=50)
    ticket_price: int
    ticket_qty: int
    payment_method: str = Field(..., max_length=50)
    transaction_id: str = Field(..., max_length=50)
    amount: float = 0
    disscount: float = 0
    transaction_fee: float
    gst: float = 0
    i_gst: float = 0
    s_gst: float = 0
    c_gst: float = 0
    total_amount: float = 0
    transaction_status: str = Field(..., pattern="^(successfully|failed|still processing)$")


class PaymentCreate(PaymentBase):
    user_id: str

class PaymentResponse(PaymentBase):
    uuid: str
    user_id: str
    ticket_type: str
    ticket_price: str
    ticket_qty: str
    payment_method: str
    transaction_id: str
    amount: float
    disscount: float
    transaction_fee: float
    gst: float
    i_gst: float
    s_gst: float    
    c_gst: float
    total_amount: float
    transaction_status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


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
        orm_mode = True


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
        orm_mode = True


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
        orm_mode = True
