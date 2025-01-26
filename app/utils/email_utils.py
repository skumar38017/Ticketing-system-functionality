# app/utils/email_utils.py
import smtplib
from email.message import EmailMessage
import os

def send_email(to_email: str, qr_code_image: bytes):
    try:
        # Get email credentials from environment variables
        from_email = os.getenv("EMAIL_ADDRESS")
        email_password = os.getenv("EMAIL_PASSWORD")

        msg = EmailMessage()
        msg["Subject"] = "Your QR Code"
        msg["From"] = from_email
        msg["To"] = to_email
        msg.set_content("Please find your QR code attached.")
        msg.add_attachment(qr_code_image, maintype="image", subtype="png", filename="qr_code.png")

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, email_password)
            server.send_message(msg)
    except Exception as e:
        print(f"Error sending email: {str(e)}")
