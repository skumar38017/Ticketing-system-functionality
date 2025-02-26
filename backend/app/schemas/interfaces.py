#  app/schemas/interfaces.py

from pydantic import BaseModel
from typing import Optional, List
from app.schemas.schema import UserResponse, PaymentResponse, QRCodeResponse, SMSResponse, EmailResponse
from datetime import datetime

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
    
# Order Interface
class OrderInterface(BaseModel):
    uuid: str
    user_uuid: str
    razorpay_order_id: str
    total_amount: float
    order_status: str
    created_at: datetime
    updated_at: datetime

# Payment Interface
class PaymentInterface(BaseModel):
    uuid: str
    user_uuid: str
    order_uuid: str
    ticket_description: str
    ticket_type: str
    ticket_price: int
    ticket_qty: int
    payment_method: str
    razorpay_payment_id: str
    transaction_id: str
    discount: float
    transaction_fee: float
    invoice_amount: float
    gst: float
    total_tax: float
    total_amount: float
    transaction_status: str
    issued_date: datetime
    updated_at: datetime

# QR Code Interface
class QRCodeInterface(BaseModel):
    uuid: str
    user_uuid: str
    payment_uuid: str
    qr_code: str
    qr_unique_id: str
    created_at: datetime
    updated_at: datetime

# SMS Interface
class SMSInterface(BaseModel):
    uuid: str
    user_uuid: str
    payment_uuid: Optional[str] = None
    qr_code_uuid: Optional[str] = None
    phone_number: str
    message: str
    created_at: datetime
    updated_at: datetime

# Email Interface
class EmailInterface(BaseModel):
    uuid: str
    user_uuid: str
    payment_uuid: Optional[str] = None
    qr_code_uuid: Optional[str] = None
    sms_uuid: Optional[str] = None
    email: str
    message: str
    created_at: datetime
    updated_at: datetime


class PaymentResponseInterface(BaseModel):
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
    payment_uuid: str
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

class UserResponseInterface(BaseModel):
    uuid: str
    name: str
    email: str
    phone_no: str
    is_active: bool
    created_at: str
    updated_at: str
