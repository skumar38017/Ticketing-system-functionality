# app/routes/websocket_routes.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket_service import WebSocketHandler
from app.utils.generate_otp import generate_otp
from app.utils.email_utils import send_email
from app.utils.qr_generator import generate_qr_code

router = APIRouter()

ws_handler = WebSocketHandler()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_handler.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "generate_otp":
                otp = generate_otp()
                await ws_handler.send_message(f"Generated OTP: {otp}")
                
                # Save OTP to session or database
                session_data = {"otp": otp}
                # Optionally save this in Redis or DB depending on your needs
                # await save_session_data(session_data)

                # Send email (real-time confirmation)
                qr_code_image = generate_qr_code("User details or QR info")
                send_email("recipient@example.com", qr_code_image)

                await ws_handler.send_message("OTP generated and email sent!")
                
            elif data == "generate_qr":
                qr_code_image = generate_qr_code("User details or QR info")
                send_email("recipient@example.com", qr_code_image)
                await ws_handler.send_message("QR code generated and email sent!")
            
    except WebSocketDisconnect:
        await ws_handler.disconnect(websocket)
