#  app/schemas/interfaces.py

from pydantic import BaseModel
from typing import List
from app.schemas.schema import UserResponse, PaymentResponse, QRCodeResponse, SMSResponse, EmailResponse

class UserInterface(BaseModel):
    uuid: str
    name: str
    email: str
    phone_no: str
    is_active: bool
    created_at: str
    updated_at: str

class VerifyOTPResponseInterface(BaseModel):
    success: bool
    message: str
    otp_status: str
    session_id: str

class PaymentInterface(BaseModel):
    uuid: str
    user_uuid: str
    ticket_description: str
    ticket_type: str
    ticket_price: int
    ticket_qty: int
    payment_method: str
    transaction_id: str
    discount: float
    transaction_fee: float
    invoice_amount: float
    gst: float
    i_gst: float
    s_gst: float
    c_gst: float
    total_tax: float = 0
    total_amount: float = 0
    transaction_status: str
    issued_date: str
    updated_at: str

class QRCodeInterface(BaseModel):
    uuid: str
    user_uuid: str
    qr_code: str
    qr_unique_id: str
    payment_uuid: str
    created_at: str
    updated_at: str

class SMSInterface(BaseModel):
    uuid: str
    user_uuid: str
    payment_uuid: str
    mobile_no: str
    message: str
    message_send_confirmation: str
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
    name: str
    email: str
    phone_no: str
    is_active: bool
    created_at: str
    updated_at: str


class PaymentResponseInterface(BaseModel):
    uuid: str
    user_uuid: str
    ticket_description: str
    ticket_type: str
    ticket_price: int
    ticket_qty: int
    payment_method: str
    transaction_id: str
    disscount: float
    transaction_fee: float
    invoice_amount: float
    gst: float
    i_gst: float
    s_gst: float
    c_gst: float
    total_tax: float = 0
    total_amount: float = 0
    transaction_status: str
    issued_date: str
    updated_at: str

class QRCodeResponseInterface(BaseModel):
    uuid: str
    user_uuid: str
    qr_code: str
    qr_unique_id: str
    payment_uuid: str
    created_at: str
    updated_at: str

class SMSResponseInterface(BaseModel):
    uuid: str
    user_uuid: str
    mobile_no: str
    message: str
    message_send_confirmation: str
    created_at: str
    updated_at: str


class EmailResponseInterface(BaseModel):
    uuid: str
    user_id: str
    email: str
    message: str
    created_at: str
    updated_at: str

