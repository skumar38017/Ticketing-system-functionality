#  app/database/models.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    uuid = Column(String(36), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone_no = Column(String(10), nullable=False)
    ticket_type = Column(String(50), nullable=False)
    ticket_price = Column(Integer, nullable=False)
    ticket_qty = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationship with other models
    payments = relationship("Payment", back_populates="user")
    qr_codes = relationship("QRCode", back_populates="user")
    sms = relationship("SMS", back_populates="user")
    emails = relationship("Email", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.uuid}, first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}', phone_no='{self.phone_no}', is_active={self.is_active}, created_at='{self.created_at}', updated_at='{self.updated_at}')>"

class Payment(Base):
    __tablename__ = "payments"

    uuid = Column(String(36), primary_key=True, default=uuid.uuid4)
    user_id =  Column(String(36), ForeignKey('users.uuid'), nullable=False)
    payment_method = Column(String(50), nullable=False)
    transaction_id = Column(String(50), nullable=False)
    transaction_status = Column(String(50), nullable=False)
    transaction_fee = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False, default=0)
    status = Column(String(50), nullable=False)
    gst = Column(Integer, nullable=False, default=0)
    i_gst = Column(Integer, nullable=False, default=0)
    s_gst = Column(Integer, nullable=False, default=0)
    c_gst = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="payments")

    def __repr__(self):
        return f"<Payment(id={self.uuid}, user_id={self.user_id}, payment_method='{self.payment_method}', amount={self.amount}, status='{self.status}', created_at='{self.created_at}', updated_at='{self.updated_at}')>"

class QRCode(Base):
    __tablename__ = "qr_codes"

    uuid = Column(String(36), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(36), ForeignKey('users.uuid'), nullable=False)
    qr_code = Column(String(50), nullable=False)
    qr_unique_id = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="qr_codes")

    def __repr__(self):
        return f"<QRCode(id={self.uuid}, user_id={self.user_id}, qr_code='{self.qr_code}', created_at='{self.created_at}', updated_at='{self.updated_at}')>"

class SMS(Base):
    __tablename__ = "sms"

    uuid = Column(String(36), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(36), ForeignKey('users.uuid'), nullable=False)
    mobile_no = Column(String(10), nullable=False)
    message = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="sms")

    def __repr__(self):
        return f"<SMS(id={self.uuid}, user_id={self.user_id}, mobile_no='{self.mobile_no}', message='{self.message}', created_at='{self.created_at}', updated_at='{self.updated_at}')>"

class Email(Base):
    __tablename__ = "emails"

    uuid = Column(String(36), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(36), ForeignKey('users.uuid'), nullable=False)
    email = Column(String(100), nullable=False)
    message = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="emails")

    def __repr__(self):
        return f"<Email(id={self.uuid}, user_id={self.user_id}, email='{self.email}', message='{self.message}', created_at='{self.created_at}', updated_at='{self.updated_at}')>"
