import qrcode
from PIL import Image, ImageDraw, ImageOps

# Data to encode
data = "https://www.example.com"

# Create QR code object
qr = qrcode.QRCode(
    version=4,  # Adjust version for desired QR complexity
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction for logo
    box_size=10,
    border=2,
)
qr.add_data(data)
qr.make(fit=True)

# Generate QR code with sleek colors
qr_img = qr.make_image(fill_color="#2c3e50", back_color="#ecf0f1").convert("RGB")  # Dark blue and light gray theme

# Add logo to the center
logo_path = "logo.png"  # Path to the logo file
logo = Image.open(logo_path).convert("RGBA")

# Resize and enhance the logo
logo_size = 100  # Logo dimensions
logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)  # Use LANCZOS for high-quality resizing

# Add a circular white border to the logo
border_size = 15
bordered_logo = Image.new("RGBA", (logo_size + border_size * 2, logo_size + border_size * 2), (255, 255, 255, 0))
mask = Image.new("L", (logo_size + border_size * 2, logo_size + border_size * 2), 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0, logo_size + border_size * 2, logo_size + border_size * 2), fill=255)
bordered_logo.paste(logo, (border_size, border_size), logo)
bordered_logo = ImageOps.fit(bordered_logo, mask.size, centering=(0.5, 0.5))
bordered_logo.putalpha(mask)

# Calculate logo position on the QR code
qr_width, qr_height = qr_img.size
logo_pos = ((qr_width - bordered_logo.size[0]) // 2, (qr_height - bordered_logo.size[1]) // 2)

# Paste the bordered logo on the QR code
qr_img = qr_img.convert("RGBA")
qr_img.paste(bordered_logo, logo_pos, mask=bordered_logo)

# Save the stylized QR code
qr_img.save("stylized_qr_with_logo.png")
print("Stylized QR code with logo saved as 'stylized_qr_with_logo.png'")
