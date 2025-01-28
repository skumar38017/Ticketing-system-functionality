#  app/utils/generate_payment_receipt.py

import os
import datetime
from app.database.models import Payment, User, QRCode
from app.database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.qr_generator import generate_qr_code  # Assuming you have this function already
from app.utils.email_utils import send_email  # Assuming you have this function already
from io import BytesIO
from fastapi import HTTPException
from fpdf import FPDF

async def generate_receipt(payment_uuid: str, db_session: AsyncSession):
    # Fetch the payment details using the payment UUID
    async with db_session() as db:
        payment = await db.execute(
            f"SELECT * FROM payments WHERE uuid = :payment_uuid",
            {"payment_uuid": payment_uuid}
        )
        payment = payment.scalars().first()

        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found.")

        user = await db.execute(
            f"SELECT * FROM users WHERE uuid = :user_uuid",
            {"user_uuid": payment.user_uuid}
        )
        user = user.scalars().first()

        # Generate a QR code for the payment
        qr_code_data = f"Payment receipt for transaction: {payment.transaction_id}"
        qr_code_image = generate_qr_code(qr_code_data)

        # Create a PDF for the payment receipt
        receipt_pdf = create_receipt_pdf(payment, user, qr_code_image)

        # Send the receipt via email
        send_receipt_email(payment, user, receipt_pdf)

        return {"message": "Payment receipt generated and emailed successfully."}

def create_receipt_pdf(payment, user, qr_code_image):
    """
    Generate a PDF receipt for the payment
    """
    # Initialize FPDF object
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Set title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Payment Receipt", ln=True, align='C')

    # Add user details
    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    pdf.cell(200, 10, txt=f"Customer Details:", ln=True)
    pdf.cell(200, 10, txt=f"Name: {user.name}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {user.email}", ln=True)
    pdf.cell(200, 10, txt=f"Phone No: {user.phone_no}", ln=True)

    # Add payment details
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Payment Details:", ln=True)
    pdf.cell(200, 10, txt=f"Transaction ID: {payment.transaction_id}", ln=True)
    pdf.cell(200, 10, txt=f"Ticket Type: {payment.ticket_type}", ln=True)
    pdf.cell(200, 10, txt=f"Ticket Quantity: {payment.ticket_qty}", ln=True)
    pdf.cell(200, 10, txt=f"Ticket Price: {payment.ticket_price} each", ln=True)
    pdf.cell(200, 10, txt=f"Total Amount: {payment.amount}", ln=True)
    pdf.cell(200, 10, txt=f"Payment Method: {payment.payment_method}", ln=True)
    pdf.cell(200, 10, txt=f"Payment Status: {payment.transaction_status}", ln=True)

    # Add GST details
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"GST Breakdown:", ln=True)
    pdf.cell(200, 10, txt=f"GST: {payment.gst}", ln=True)
    pdf.cell(200, 10, txt=f"CGST: {payment.c_gst}", ln=True)
    pdf.cell(200, 10, txt=f"SGST: {payment.s_gst}", ln=True)
    pdf.cell(200, 10, txt=f"IGST: {payment.i_gst}", ln=True)

    # Add QR code image
    pdf.ln(10)
    pdf.image(qr_code_image, x=10, y=pdf.get_y(), w=30)

    # Add footer with date
    pdf.ln(40)
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(200, 10, txt=f"Date: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')

    # Save PDF to a BytesIO object to return it for emailing
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    return pdf_output

def send_receipt_email(payment, user, receipt_pdf):
    """
    Send the payment receipt via email to the user.
    """
    subject = f"Payment Receipt for Transaction {payment.transaction_id}"
    message = f"Dear {user.name},\n\nYour payment for transaction {payment.transaction_id} has been successfully processed.\nPlease find attached your payment receipt."

    # Convert BytesIO PDF to file-like object
    receipt_pdf.seek(0)
    send_email(user.email, subject, message, receipt_pdf)
