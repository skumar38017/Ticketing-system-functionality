#  app/middleware/cors_middleware.py

from starlette.middleware.cors import CORSMiddleware
from typing import List, Optional

class CustomCORSMiddleware(CORSMiddleware):
    def __init__(self, 
                 app,
                 allow_origins: Optional[List[str]] = None, 
                 allow_credentials: bool = True, 
                 allow_methods: Optional[List[str]] = None, 
                 allow_headers: Optional[List[str]] = None):
        """
        Custom CORS Middleware.
        
        - Allows customization of CORS headers.
        """
        super().__init__(
            app,
            allow_origins=allow_origins or ["*"],  # Default to allow all origins
            allow_credentials=allow_credentials,
            allow_methods=allow_methods or ["*"],  # Default to allow all methods
            allow_headers=allow_headers or ["*"],  # Default to allow all headers
        )
