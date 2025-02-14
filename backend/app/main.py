#  Neon-Stdio-Holi-T25/app/main.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse
from app.routes import user_routes, webhook_routes, websocket_routes, qr_code_routes
from app.database.database import get_db_connection, get_db, login_to_database
from app.database.redisclient import redis_client
from app.database.models import User
from fastapi import APIRouter, WebSocket
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

from app.services.otp_service import OTPService


# Initialize OTPTask and OTPService
router = APIRouter()
ws_handler = WebSocketHandler()


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
    openapi_url="/openapi.json",  # Always enable OpenAPI schema
    docs_url="/docs",            # Always enable Swagger UI
    redoc_url="/redoc",          # Always enable ReDoc
)

# Add middleware separately
app.add_middleware(RedisSessionMiddleware)
app.add_middleware(CustomCORSMiddleware)

#  Root 
@app.get("/", include_in_schema=True)
async def index():
    """
    Root endpoint.
    """
    return {"message": "Ticket Management System"}

# Include routes
app.include_router(user_routes.router)
# app.include_router(qr_code_routes.router)
# app.include_router(webhook_routes.router)
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
        print("Starting application and checking DB connection...")
        await login_to_database()
        print("DB connection successful.")
        print("Starting application and checking Redis connection...")
        redis_client.connect()
        print("Redis connection successful.")
            # Print out all registered routes
        for route in app.routes:
            print(route.path, route.name)
        # Placeholder for startup logic (e.g., database initialization or worker setup)
        logger.info("Startup tasks completed successfully.")
    except Exception as e:
        logger.error(f"Startup tasks failed: {e}")
        sys.exit(1)  # Exit the application if setup fails

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
