#  app/utils/qr_generator.py

import qrcode
from io import BytesIO

def generate_qr_code(user_details):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(user_details)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.getvalue()
