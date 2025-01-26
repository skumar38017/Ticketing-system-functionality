# app/middleware/session_middleware.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from redis import Redis
import pickle
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedisSessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_url: str = os.getenv('REDIS_URL')):
        super().__init__(app)
        self.redis = Redis.from_url(redis_url)
        logger.info("Redis session middleware initialized.")

    async def dispatch(self, request, call_next):
        """
        Middleware to manage session using Redis.
        """
        session_id = request.cookies.get('session_id')
        if session_id:
            session_data = self.redis.get(session_id)
            if session_data:
                request.state.session = pickle.loads(session_data)
            else:
                request.state.session = {}
        else:
            request.state.session = {}

        # Proceed with the request and capture the response
        response = await call_next(request)

        # Store session data back to Redis
        if hasattr(request, 'state') and hasattr(request.state, 'session'):
            session_data = pickle.dumps(request.state.session)
            if not session_id:
                session_id = os.urandom(24).hex()  # Generate a new session ID
                response.set_cookie('session_id', session_id, httponly=True)  # Secure cookie

            self.redis.set(session_id, session_data)

        return response
