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
        self.otp_attempts: Dict[str, int] = {}  # Track attempts for each phone number


    #  Connect and disconnect methods
    async def connect(self, websocket: WebSocket):
        """
        Handles a new WebSocket connection.
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        self.logger.info(f"New WebSocket connection: {websocket.client}")
        
        # Log message in the terminal for knowledge
        print(f"New WebSocket connection established: {websocket.client}")

    # Disconnect method
    async def disconnect(self, websocket: WebSocket):
        """
        Disconnect a WebSocket connection and clean up subscriptions.
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            self.logger.info(f"WebSocket disconnected: {websocket.client}")
        
        # Log message in the terminal for knowledge
        print(f"WebSocket disconnected: {websocket.client}")

        # Clean up subscriptions for the disconnected WebSocket
        for phone_no, websockets in self.subscriptions.items():
            if websocket in websockets:
                websockets.remove(websocket)
                self.logger.info(f"WebSocket unsubscribed from {phone_no}")

    # Send message methods
    async def send_message(self, websocket: WebSocket, message: str = "Default message"):
        """
        Send a message to a specific WebSocket connection.
        """
        if websocket in self.active_connections:
            await websocket.send_text(message)

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

    async def send_otp_with_status(self, phone_no: str, otp: str, attempt: int):
        """
        Sends the OTP to all WebSocket connections for the given phone number with status updates.
        Includes retry logic with up to 3 attempts.
        """
        # Increment attempt count
        if phone_no not in self.otp_attempts:
            self.otp_attempts[phone_no] = 0
        self.otp_attempts[phone_no] += 1

        status_message = f"Attempt {self.otp_attempts[phone_no]}: OTP for {phone_no}: {otp}"

        for connection in self.active_connections:
            try:
                await connection.send_text(status_message)
            except WebSocketDisconnect:
                self.active_connections.remove(connection)

        if self.otp_attempts[phone_no] >= 3:
            await self.send_task_status(phone_no, "OTP delivery failed after 3 attempts")
            self.otp_attempts[phone_no] = 0  # Reset attempt count after 3 failed attempts
        else:
            # If delivery is successful, mark as success
            await self.send_task_status(phone_no, f"OTP delivered to {phone_no} successfully.")

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
        """
        Send task status (e.g., delivery success or failure) to the subscribed WebSocket clients.
        """
        if phone_no in self.subscriptions:
            message = {"phone_no": phone_no, "status": status}
            for websocket in self.subscriptions[phone_no]:
                if websocket in self.active_connections:
                    try:
                        await websocket.send_json(message)
                    except WebSocketDisconnect:
                        self.logger.warning(f"Connection lost with WebSocket: {websocket.client}")
                        await self.disconnect(websocket)
                        self.subscriptions[phone_no].remove(websocket)

    def get_connection_by_phone(self, phone_no: str) -> List[WebSocket]:
        """
        Retrieve WebSocket connections associated with a phone number.
        """
        return self.subscriptions.get(phone_no, [])

    async def broadcast_order_created(self, transaction_id: str, transaction_status: str, user_uuid: str):
        message = f"Order with transaction ID {transaction_id}, status {transaction_status} created for user {user_uuid}"
        await self.broadcast(message)