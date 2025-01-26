#  app/schemas/user_schema.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
import uuid

# User schema
class UserBase(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: EmailStr
    phone_no: str = Field(..., max_length=10, min_length=10)
    ticket_type: str = Field(..., max_length=50)
    ticket_price: int
    ticket_qty: int
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    uuid: str
    first_name: str
    last_name: str
    email: str
    phone_no: str
    ticket_type: str
    ticket_price: int
    ticket_qty: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Payment schema
class PaymentBase(BaseModel):
    payment_method: str = Field(..., max_length=50)
    transaction_id: str = Field(..., max_length=50)
    transaction_status: str = Field(..., max_length=50)
    transaction_fee: int
    amount: int = 0
    status: str = Field(..., max_length=50)
    gst: int = 0
    i_gst: int = 0
    s_gst: int = 0
    c_gst: int = 0


class PaymentCreate(PaymentBase):
    user_id: str


class PaymentResponse(PaymentBase):
    uuid: str
    user_id: str
    payment_method: str
    transaction_id: str
    transaction_status: str
    transaction_fee: int
    amount: int
    status: str
    gst: int
    i_gst: int
    s_gst: int    
    c_gst: int
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


class QRCodeResponse(QRCodeBase):
    uuid: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# SMS schema
class SMSBase(BaseModel):
    mobile_no: str = Field(..., max_length=10, min_length=10)
    message: str = Field(..., max_length=50)


class SMSCreate(SMSBase):
    user_id: str


class SMSResponse(SMSBase):
    uuid: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Email schema
class EmailBase(BaseModel):
    email: EmailStr
    message: str


class EmailCreate(EmailBase):
    user_id: str


class EmailResponse(EmailBase):
    uuid: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
