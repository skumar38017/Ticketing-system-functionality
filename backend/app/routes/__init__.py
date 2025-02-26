#  app/routes/__init__.py

# app/routes/__init__.py

from .user_routes import router as user_router
from .ticket_routes import router as ticket_router
from .qr_code_routes import router as qr_code_router
from .webhook_routes import webhook_router  # Add this line
from .websocket_routes import router as websocket_router

# Export all routers
__all__ = [
    "user_router",
    "ticket_router",
    "qr_code_router",
    "webhook_router",  # Add this line
    "websocket_router",
]