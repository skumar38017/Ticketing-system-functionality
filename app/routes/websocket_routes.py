#  app/routes/websocket_routes.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

connected_clients = []

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for client in connected_clients:
                if client != websocket:
                    await client.send_text(f"Message from client: {data}")
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
