    #  app/database/models.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum,Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime
from app.database.database import Base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    # Columns
    uuid = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    phone_no = Column(String(16), nullable=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships with other models
    payments = relationship("Payment", back_populates="user")
    qr_codes = relationship("QRCode", back_populates="user")
    sms = relationship("SMS", back_populates="user")
    emails = relationship("Email", back_populates="user")

    # Updated __repr__ for consistency
    def __repr__(self):
        return (f"<User(id={self.uuid}, name='{self.name}', email='{self.email}', "
                f"phone_no='{self.phone_no}', is_active={self.is_active}, "
                f"created_at='{self.created_at}', updated_at='{self.updated_at}')>")


class Payment(Base):
    __tablename__ = "payments"

    # Columns
    uuid = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_uuid = Column(String(36), ForeignKey('users.uuid'), nullable=False)
    ticket_description = Column(String(500), nullable=False)  # E.g., Event ticket description
    ticket_type = Column(String(50), nullable=False)  # E.g., Regular, VIP
    ticket_price = Column(Integer, nullable=False)  # Price per ticket
    ticket_qty = Column(Integer, nullable=False)  # Number of tickets purchased
    payment_method = Column(String(50), nullable=False)  # E.g., Debit Card, UPI, etc.
    transaction_id = Column(String(50), nullable=False)  # Transaction reference ID
    discount = Column(Float, nullable=False, default=0.0)  # Discount amount
    transaction_fee = Column(Float, nullable=False)  # Fee associated with the payment
    invoice_amount = Column(Float, nullable=False, default=0.0)  # Invoice amount before taxes
    gst = Column(Float, nullable=False, default=0.0)  # Total GST applied
    i_gst = Column(Float, nullable=False, default=0.0)  # IGST applied
    s_gst = Column(Float, nullable=False, default=0.0)  # SGST applied
    c_gst = Column(Float, nullable=False, default=0.0)  # CGST applied
    total_tax = Column(Float, nullable=False, default=0.0)  # Total tax applied
    total_amount = Column(Float, nullable=False, default=0.0)  # Total amount after taxes and fees
    transaction_status = Column(Enum('successfully', 'failed', 'still processing', 'cancelled', 'due', name='payment_status'), nullable=False)  # Payment status
    issued_date = Column(DateTime, default=datetime.datetime.utcnow)  # Record creation time
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)  # Last update time

    # Relationship with User model
    user = relationship("User", back_populates="payments")
    qr_codes = relationship("QRCode", back_populates="payment")
    sms = relationship("SMS", back_populates="payment")
    emails = relationship("Email", back_populates="payment")  # Ensure this is here

    # __repr__ for debugging and logging
    def __repr__(self):
        return (f"<Payment(uuid={self.uuid}, user_uuid={self.user_uuid}, ticket_description='{self.ticket_description}', "
                f"ticket_type='{self.ticket_type}', ticket_price={self.ticket_price}, ticket_qty={self.ticket_qty}, "
                f"payment_method='{self.payment_method}', transaction_id='{self.transaction_id}', transaction_fee={self.transaction_fee}, "
                f"invoice_amount={self.invoice_amount}, discount={self.discount}, gst={self.gst}, i_gst={self.i_gst}, "
                f"s_gst={self.s_gst}, c_gst={self.c_gst}, total_tax={self.total_tax}, total_amount={self.total_amount}, "
                f"transaction_status='{self.transaction_status}', issued_date='{self.issued_date}', updated_at='{self.updated_at}')>")
    
class QRCode(Base):
    __tablename__ = "qr_codes"
    # Columns
    uuid = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # Unique identifier for QR Code
    user_uuid = Column(String(36), ForeignKey('users.uuid'), nullable=False)  # Link to the User
    payment_uuid = Column(String(36), ForeignKey('payments.uuid'), nullable=False)  # Link to the Payment
    qr_code = Column(String(255), nullable=False)  # QR Code data (e.g., base64 or file path)
    qr_unique_id = Column(String(50), nullable=False, unique=True)  # Unique identifier for the QR Code
    created_at = Column(DateTime, default=datetime.datetime.utcnow)  # Record creation timestamp
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)  # Record update timestamp

    # Relationships
    user = relationship("User", back_populates="qr_codes")  # Relationship with User model
    payment = relationship("Payment", back_populates="qr_codes")  # Relationship with Payment model
    sms = relationship("SMS", back_populates="qr_code")
    emails = relationship("Email", back_populates="qr_code")

    # __repr__ for debugging and logging
    def __repr__(self):
        return (f"<QRCode(uuid={self.uuid}, user_uuid={self.user_uuid}, payment_uuid={self.payment_uuid}, "
                f"qr_code='{self.qr_code}', qr_unique_id='{self.qr_unique_id}', created_at='{self.created_at}', "
                f"updated_at='{self.updated_at}')>")
    
class SMS(Base):
    __tablename__ = "sms"
    # Columns
    uuid = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # Unique identifier for SMS
    user_uuid = Column(String(36), ForeignKey('users.uuid'), nullable=False)  # Link to the User
    payment_uuid = Column(String(36), ForeignKey('payments.uuid'), nullable=False)  # Link to the Payment
    qr_code_uuid = Column(String(36), ForeignKey('qr_codes.uuid'), nullable=False)  # Link to the QR Code
    mobile_no = Column(String(10), nullable=False)  # Mobile number to send the SMS
    message = Column(String(500), nullable=False)  # The content of the SMS
    message_send_confirmation = Column(Enum('successfully', 'failed', name='sms_status'), nullable=False)  # Status of the SMS
    created_at = Column(DateTime, default=datetime.datetime.utcnow)  # Record creation timestamp
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)  # Record update timestamp

    # Relationships
    user = relationship("User", back_populates="sms")  # Relationship with User model
    payment = relationship("Payment", back_populates="sms")  # Relationship with Payment model
    qr_code = relationship("QRCode", back_populates="sms")  # Relationship with QRCode model
    emails = relationship("Email", back_populates="sms")

    # __repr__ for debugging and logging
    def __repr__(self):
        return (f"<SMS(uuid={self.uuid}, user_uuid={self.user_uuid}, payment_uuid={self.payment_uuid}, "
                f"qr_code_uuid={self.qr_code_uuid}, mobile_no='{self.mobile_no}', message='{self.message}', "
                f"message_send_confirmation='{self.message_send_confirmation}', created_at='{self.created_at}', "
                f"updated_at='{self.updated_at}')>")

class Email(Base):
    __tablename__ = "emails"
    uuid = Column(String(36), primary_key=True, default=uuid.uuid4)
    user_uuid = Column(String(36), ForeignKey('users.uuid'), nullable=False)
    email = Column(String(100), nullable=False)
    message = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="emails")
    payment = relationship("Payment", back_populates="emails")  # Changed this from 'Payment' to 'payment'
    qr_code = relationship("QRCode", back_populates="emails")
    sms = relationship("SMS", back_populates="emails")
    
    def __repr__(self):
        return f"<Email(id={self.uuid}, user_id={self.user_uuid}, email='{self.email}', message='{self.message}', created_at='{self.created_at}', updated_at='{self.updated_at}')>"
    