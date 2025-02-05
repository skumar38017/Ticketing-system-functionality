# app/services/websocket_service.py
import asyncio
import logging
from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict


class WebSocketHandler:
    def __init__(self):
        self.active_connections: List[WebSocket] = []  # List to track all active connections
        self.logger = logging.getLogger("uvicorn.error")
        self.subscriptions: Dict[str, List[WebSocket]] = {}  # Map of phone_no to list of WebSocket connections

    #  Connect and disconnect methods
    async def connect(self, websocket: WebSocket):
        """
        Handles a new WebSocket connection.
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        self.logger.info(f"New WebSocket connection: {websocket.client}")

    # self.send_message(websocket, "Welcome to the WebSocket server!")
    async def disconnect(self, websocket: WebSocket):
        """
        Disconnect a WebSocket connection and clean up subscriptions.
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            self.logger.info(f"WebSocket disconnected: {websocket.client}")

        # Clean up subscriptions for the disconnected WebSocket
        for phone_no, websockets in self.subscriptions.items():
            if websocket in websockets:
                websockets.remove(websocket)
                self.logger.info(f"WebSocket unsubscribed from {phone_no}")

    #  Send message methods
    async def send_message(self, websocket: WebSocket, message:  str = "Default message"):
        """
        Send a message to a specific WebSocket connection.
        """
        if websocket in self.active_connections:
            await websocket.send_text(message)

    def subscribe(self, phone_no: str, websocket: WebSocket):
        """
        Subscribe a WebSocket connection to updates for a specific phone number.
        """
        if phone_no not in self.subscriptions:
            self.subscriptions[phone_no] = []
        self.subscriptions[phone_no].append(websocket)
        print(f"WebSocket {websocket} subscribed to {phone_no}")

    async def send_otp(self, mobile_no: str, otp: str):
        """
        Sends the OTP to all active WebSocket connections.
        """
        for connection in self.active_connections:
            try:
                await connection.send_text(f"OTP for {mobile_no}: {otp}")
            except WebSocketDisconnect:
                print("A connection was disconnected while sending OTP.")
                self.active_connections.remove(connection)

    def subscribe(self, phone_no: str, websocket: WebSocket):
        """
        Subscribe a WebSocket connection to updates for a specific phone number.
        """
        if phone_no not in self.subscriptions:
            self.subscriptions[phone_no] = []
        self.subscriptions[phone_no].append(websocket)
        self.logger.info(f"WebSocket {websocket.client} subscribed to {phone_no}")

    async def send_otp(self, phone_no: str, otp: str):
        """
        Sends the OTP to all WebSocket connections subscribed to a phone number.
        """
        if phone_no in self.subscriptions:
            for websocket in self.subscriptions[phone_no]:
                try:
                    await websocket.send_text(f"OTP for {phone_no}: {otp}")
                except WebSocketDisconnect:
                    self.logger.warning("A WebSocket was disconnected while sending OTP.")
                    await self.disconnect(websocket)

    async def broadcast(self, message: str, sender_websocket: WebSocket = None):
        """
        Broadcasts a message to all connected WebSocket clients except the sender.
        """
        for websocket in self.active_connections:
            if websocket != sender_websocket:
                try:
                    await websocket.send_text(f"Broadcast: {message}")
                except WebSocketDisconnect:
                    self.logger.warning(f"Lost connection with WebSocket: {websocket.client}")
                    await self.disconnect(websocket)

    async def send_task_status(self, phone_no: str, status: str):
        if phone_no in self.subscriptions:
            message = {"phone_no": phone_no, "status": status}
            for websocket in self.subscriptions[phone_no]:
                if websocket in self.active_connections:
                    try:
                        await websocket.send_json({"phone_no": phone_no, "status": status})
                    except WebSocketDisconnect:
                        self.logger.warning(f"Connection lost with WebSocket: {websocket.client}")
                        await self.disconnect(websocket)
                        self.subscriptions[phone_no].remove(websocket)

    def get_connection_by_phone(self, phone_no: str) -> List[WebSocket]:
        """
        Retrieve WebSocket connections associated with a phone number.
        """
        return self.subscriptions.get(phone_no, [])

