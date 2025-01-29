#  Neon-Stdio-Holi-T25/app/main.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse
from app.routes import user_routes, webhook_routes, websocket_routes
from app.workers.celery_app import celery_app
from app.database.database import get_db_connection
from app.database.models import User
from app.tasks.email_tasks import send_welcome_email
from app.services.websocket_service import WebSocketHandler
from app.config import config
from app.settings import settings
from app.middleware.cors_middleware import CustomCORSMiddleware
from app.middleware.session_middleware import RedisSessionMiddleware
from io import BytesIO
from pyzbar.pyzbar import decode
from PIL import Image
import asyncio
import logging
import sys
import qrcode
import uvicorn

logger = logging.getLogger(__name__)

# Conditional URLs based on DEV_MODE
if not settings.DEV_MODE:
    openapi_url = None
    docs_url = None
    redoc_url = None
else:
    openapi_url = "/openapi.json"
    docs_url = "/"
    redoc_url = "/redoc"

app = FastAPI(
    title="Ticket Management System",
    description="This is a ticket management system for the Neon-Stdio Holi-T25 course.",
    version="1.1.0",
    openapi_url=openapi_url,
    docs_url=docs_url,
    redoc_url=redoc_url,
)

# Add middleware separately
app.add_middleware(RedisSessionMiddleware, redis_url=config.redis_result_url)
app.add_middleware(CustomCORSMiddleware)

# Include routes
app.include_router(user_routes.router)
app.include_router(webhook_routes.router)
app.include_router(websocket_routes.router)

# Initialize WebSocketHandler
ws_handler = WebSocketHandler()

@app.on_event("startup")
async def startup_event():
    """
    Event handler that runs on application startup.
    """
    logger.info(f"Application started in {'Development' if settings.DEV_MODE else 'Production'} mode.")
    logger.info("Running setup tasks.")
    try:
        # Placeholder for startup logic (e.g., database initialization or worker setup)
        logger.info("Startup tasks completed successfully.")
    except Exception as e:
        logger.error(f"Startup tasks failed: {e}")
        sys.exit(1)  # Exit the application if setup fails


#  
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint to handle client-server real-time communication.
    """
    await ws_handler.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await ws_handler.send_message(f"Message received: {data}")
    except WebSocketDisconnect:
        await ws_handler.disconnect(websocket)

#  
@app.get("/", include_in_schema=False)
async def index():
    """
    Root endpoint.
    """
    return {"message": "Ticket Management System"}

# 
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom exception handler for HTTP exceptions.
    """
    if not settings.DEV_MODE:
        # Change 422 to 400 in production
        status_code = 400 if exc.status_code == 422 else exc.status_code
        return JSONResponse(
            status_code=status_code,
            content={"message": "Bad Request", "path": request.url.path},
        )
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
