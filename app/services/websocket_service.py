# app/services/websocket_service.py
import asyncio
from fastapi import WebSocket, WebSocketDisconnect
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
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                print("A connection was disconnected while sending a message.")
                self.active_connections.remove(connection)

    async def broadcast(self, message: str, websocket: WebSocket):
        """
        Broadcasts a message to all connected clients except the sender.
        """
        for connection in self.active_connections:
            if connection != websocket:
                try:
                    await connection.send_text(f"Message from client: {message}")
                except WebSocketDisconnect:
                    print(f"Connection lost with client: {connection.client}")
                    self.active_connections.remove(connection)
