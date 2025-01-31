# app/middleware/session_middleware.py

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from redis import Redis
import pickle
import os
import logging
from fastapi import Request, Response
from typing import Optional
from app.config import config
from app.services.websocket_service import WebSocketHandler
from app.database.redisclient import redis_client  # Import the RedisClient instance


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedisSessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, paths_to_handle=None):
        """
        Initialize the Redis session middleware.

        Args:
            app: The FastAPI application.
            paths_to_handle: List of paths to manage sessions for.
        """
        super().__init__(app)
        self.redis = redis_client.redis  # Use the shared Redis client instance
        if not self.redis:
            raise ValueError("Redis client instance not initialized properly.")
        self.ws_handler = WebSocketHandler()  # WebSocket handler
        self.paths_to_handle = paths_to_handle or ["/register"]  # Default to "/register"
        logger.info("Redis session middleware initialized.")

    async def dispatch(self, request: Request, call_next):
        """
        Middleware to manage session using Redis for specific requests.

        Args:
            request: The incoming HTTP request.
            call_next: The next middleware or route handler.

        Returns:
            Response: The HTTP response.
        """
        try:
            # Check if the session should be handled for this request
            if request.url.path in self.paths_to_handle:
                session_id = request.cookies.get("session_id")
                if not session_id:
                    # Generate a new session ID only when required
                    session_id = os.urandom(24).hex()
                    request.state.session = {}
                    logger.info(f"New session created: {session_id}")
                else:
                    # Retrieve binary session data from Redis
                    session_data = self.redis.get(f"session:{session_id}")
                    if session_data:
                        # Deserialize the binary data
                        request.state.session = pickle.loads(session_data)
                        logger.info(f"Loaded session data for session_id: {session_id}")
                    else:
                        request.state.session = {}
                        logger.info(f"No session data found for session_id: {session_id}, starting new session.")

                # Process the request
                response = await call_next(request)

                # Save session data back to Redis
                if hasattr(request.state, "session"):
                    session_data = pickle.dumps(request.state.session)  # Serialize session data
                    self.redis.setex(
                        f"session:{session_id}",
                        config.expiration_time,
                        session_data,
                    )
                    if not request.cookies.get("session_id"):
                        response.set_cookie(
                            "session_id",
                            session_id,
                            httponly=True,
                            secure=True,
                            samesite="lax",
                            max_age=config.expiration_time,
                        )
                        await self.ws_handler.send_message(f"New session created: {session_id}")

                return response

            # Skip session management for other routes
            return await call_next(request)

        except Exception as e:
            logger.error(f"Error in Redis session middleware: {e}")
            return JSONResponse(
                status_code=500,
                content={"message": "Internal server error"},
            )