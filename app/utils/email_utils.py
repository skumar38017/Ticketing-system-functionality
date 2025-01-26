#  app/utils/email_utils.py

import smtplib
from email.message import EmailMessage

def send_email(to_email: str, qr_code_image: bytes):
    try:
        print('to_email', to_email)
        msg = EmailMessage()
        msg["Subject"] = "Your QR Code"
        msg["From"] = "parmarsa8857@gmail.com"
        msg["To"] = to_email
        msg.set_content("Please find your QR code attached.")
        msg.add_attachment(qr_code_image, maintype="image", subtype="png", filename="qr_code.png")

        print('mail send')
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("parmarsa8857@gmail.com", "ttxg kbyd ixqo uiqv")
            server.send_message(msg)
    except Exception as e:
        print(f"Error sending email: {str(e)}")
