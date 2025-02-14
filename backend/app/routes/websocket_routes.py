# app/routes/websocket_routes.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket_service import WebSocketHandler

router = APIRouter()
ws_handler = WebSocketHandler()


@router.websocket("/ws")
async def websocket_general_endpoint(websocket: WebSocket):
    """
    General WebSocket endpoint for real-time communication.
    """
    await ws_handler.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await ws_handler.send_message(websocket, f"Message received: {data}")
    except WebSocketDisconnect:
        await ws_handler.disconnect(websocket)

#  
@router.websocket("/ws/otp_status")
async def websocket_otp_status_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint to send OTP status updates.
    This endpoint listens for OTP task-related requests and sends updates.
    """
    await ws_handler.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data.startswith("subscribe:"):
                phone_no = data.split(":")[1]
                print(f"Client subscribed to OTP status updates for phone: {phone_no}")
                await ws_handler.subscribe(phone_no, websocket)
                await ws_handler.send_message(websocket, f"Subscribed to OTP updates for {phone_no}.")
            elif data == "ping":
                await websocket.send_text("pong")
            else:
                await ws_handler.send_message(websocket, "Unhandled message format.")
    except WebSocketDisconnect:
        await ws_handler.disconnect(websocket)


@router.websocket("/ws/otp_status")
async def websocket_otp_status_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint to send OTP status updates.
    This endpoint listens for OTP task-related requests and sends updates.
    """
    await ws_handler.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data.startswith("subscribe:"):
                phone_no = data.split(":")[1]
                print(f"Client subscribed to OTP status updates for phone: {phone_no}")
                await ws_handler.subscribe(phone_no, websocket)
                await ws_handler.send_message(websocket, f"Subscribed to OTP updates for {phone_no}.")
            elif data == "ping":
                await websocket.send_text("pong")
            else:
                await ws_handler.send_message(websocket, "Unhandled message format.")
    except WebSocketDisconnect:
        await ws_handler.disconnect(websocket)

@router.websocket("/ws/session")
async def websocket_session_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for session notifications and health checks.
    """
    await ws_handler.connect(websocket)
    try:
        while True:
            # Keep the connection alive and handle incoming messages
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
            else:
                await ws_handler.send_message(f"Unhandled message: {data}")
    except WebSocketDisconnect:
        await ws_handler.disconnect(websocket)
