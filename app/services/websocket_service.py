# app/services/websocket_service.py
from fastapi import WebSocket
from typing import List

class WebSocketHandler:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """
        Handles a new WebSocket connection.
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"New connection: {websocket.client}")

    async def disconnect(self, websocket: WebSocket):
        """
        Handles WebSocket disconnection.
        """
        self.active_connections.remove(websocket)
        print(f"Disconnected: {websocket.client}")

    async def send_message(self, message: str):
        """
        Sends a message to all active WebSocket connections.
        """
        for connection in self.active_connections:
            await connection.send_text(message)

    async def broadcast(self, message: str, websocket: WebSocket):
        """
        Broadcasts a message to all connected clients except the sender.
        """
        for connection in self.active_connections:
            if connection != websocket:
                await connection.send_text(f"Message from client: {message}")
