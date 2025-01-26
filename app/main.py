#  Neon-Stdio-Holi-T25/app/main.py

from fastapi import FastAPI
from app.routes import user_routes
from app.workers.celery_app import celery_app
from app.routes import user_routes, webhook_routes, websocket_routes
from app.workers.celery_app import celery_app

import json
import qrcode
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse
from app.database.database import get_db_connection
from app.models import UserRegister
from app.tasks import send_welcome_email
from app.websocket import WebSocketHandler
from io import BytesIO
from pyzbar.pyzbar import decode
from PIL import Image


# Conditional URLs based on DEV_MODE
if not settings.DEV_MODE:
    openapi_url = None
    docs_url = None
    redoc_url = None

# Include routes
app.include_router(user_routes.router)
app.include_router(webhook_routes.router)
app.include_router(websocket_routes.router)

app = FastAPI(
    title="Ticket Management System",
    description="This is a ticket management system for the Neon-Stdio Holi-T25 course.",
    version="0.1.0",
    docs_url="/",
    redoc_url="/redoc",
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS
    if isinstance(settings.CORS_ORIGINS, list)
    else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Configure OpenAPI
openapi_url = app.openapi_url
docs_url = app.docs_url
redoc_url = app.redoc_url
app.openapi_schema = None
app.openapi = app.get_openapi(
    openapi_url=openapi_url,
    docs_url=docs_url,
    redoc_url=redoc_url,
)

@app.on_event("startup")
async def startup_event():
    """
    Event handler that runs on application startup.
    """
    logger.info(
        f"Application started in {'Development' if settings.DEV_MODE else 'Production'} mode."
    )

    logger.info("Application startup: Running setup tasks.")
    global face_analyser
    try:
        await run_parallel_tasks()
        face_analyser = FaceAnalyser(model_path="app/export.pkl")
        await asyncio.sleep(2)
        sync_worker.start()
        logger.info("Setup tasks completed successfully.")
    except Exception as e:
        logger.error(f"Setup tasks failed: {e}")
        sys.exit(1)  # Optionally exit the application if setup fails

# Include routes
app.include_router(user_routes.router)

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


@app.get("/", include_in_schema=False, response_class=JSONResponse)
async def index():
    return {"message": "Ticket Management System"}
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if not settings.DEV_MODE:
        # Change 422 to 400 if in production
        dev_status_code = 400 if exc.status_code == 422 else exc.status_code
        return JSONResponse(
            status_code=dev_status_code,
            content={
                "message": "Bad Request",
                "path": request.url.path,
            },
        )
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
