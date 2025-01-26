#  app/schemas/interfaces.py

from pydantic import BaseModel
from typing import List
from app.schemas.schema import UserResponse, PaymentResponse, QRCodeResponse, SMSResponse, EmailResponse

class UserInterface(BaseModel):
    uuid: str
    first_name: str
    last_name: str
    email: str
    phone_no: str
    ticket_type: str
    ticket_price: int
    ticket_qty: int
    is_active: bool
    created_at: str
    updated_at: str

class PaymentInterface(BaseModel):
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
    created_at: str
    updated_at: str

class QRCodeInterface(BaseModel):
    uuid: str
    user_id: str
    qr_code: str
    qr_unique_id: str
    created_at: str
    updated_at: str

class SMSInterface(BaseModel):
    uuid: str
    user_id: str
    mobile_no: str
    message: str
    created_at: str
    updated_at: str

class EmailInterface(BaseModel):
    uuid: str
    user_id: str
    email: str
    message: str
    created_at: str
    updated_at: str

class UserResponseInterface(BaseModel):
    uuid: str
    first_name: str
    last_name: str
    email: str
    phone_no: str
    ticket_type: str
    ticket_price: int
    ticket_qty: int
    is_active: bool
    created_at: str
    updated_at: str

class PaymentResponseInterface(BaseModel):
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
    created_at: str
    updated_at: str

class QRCodeResponseInterface(BaseModel):
    uuid: str
    user_id: str
    qr_code: str
    qr_unique_id: str
    created_at: str
    updated_at: str

class SMSResponseInterface(BaseModel):
    uuid: str
    user_id: str
    mobile_no: str
    message: str
    created_at: str
    updated_at: str

class EmailResponseInterface(BaseModel):
    uuid: str
    user_id: str
    email: str
    message: str
    created_at: str
    updated_at: str
