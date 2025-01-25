import json
import qrcode
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse
from app.database import get_db_connection
from app.models import UserRegister
from app.tasks import send_welcome_email
from app.websocket import WebSocketHandler
from io import BytesIO
from pyzbar.pyzbar import decode
from PIL import Image

app = FastAPI()

# Initialize WebSocketHandler
ws_handler = WebSocketHandler()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_handler.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await ws_handler.send_message(f"Message received: {data}")
    except WebSocketDisconnect:
        await ws_handler.disconnect(websocket)

@app.post("/register")
async def register_user(user: UserRegister):
    try:
        user_details = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone_no": user.phone_no
        }

        # Generate QR code
        qr_code_image = generate_qr_code(user_details)

        # Save user and send email (async task)
        print('before register user.email', user.email)
        send_welcome_email.delay(user.email, qr_code_image)
        print('After register user.email', user.email)

        return JSONResponse(
            status_code=200,
            content={"message": "User registered successfully and QR code sent to email."}
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

@app.post("/validate_qr")
async def validate_qr(file: UploadFile):
    try:
        # Open the uploaded file as an image
        img = Image.open(file.file)
        
        # Decode the QR code from the image
        decoded_data = decode(img)
        if not decoded_data:
            raise HTTPException(status_code=400, detail="No QR code found in the image.")
        
        # Decode QR code data to JSON
        qr_data = decoded_data[0].data.decode('utf-8')
        user_data = json.loads(qr_data)
        
        # Validate the user from database (can be replaced with custom logic)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (user_data["email"],))
        user = cursor.fetchone()
        conn.close()

        if user:
            return RedirectResponse(url="/success", status_code=303)
        else:
            raise HTTPException(status_code=400, detail="Invalid QR code or user not found.")
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

def generate_qr_code(user_details):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(user_details)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.getvalue()

@app.get("/success")
async def success_page():
    return JSONResponse(content={"message": "QR Code validated successfully. Welcome!"})

@app.get("/error")
async def error_page():
    return JSONResponse(content={"message": "Invalid QR Code. Please try again."})

@app.get("/")
async def index():
    return {"message": "Hello World"}
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)