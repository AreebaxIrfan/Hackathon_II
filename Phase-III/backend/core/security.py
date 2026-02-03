from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi import FastAPI
import os

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

def setup_security(app: FastAPI):
    """
    Configure security measures for the application.
    """
    # Add rate limiting
    app.state.limiter = limiter
    app.add_exception_handler(_rate_limit_exceeded_handler)

    # Additional security configurations can be added here
    # - Security headers
    # - Input sanitization
    # - Other security middleware