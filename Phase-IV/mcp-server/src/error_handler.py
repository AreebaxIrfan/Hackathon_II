"""
Error handling and logging infrastructure for MCP tools
"""
import logging
from typing import Callable, Awaitable
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse


class ErrorHandlerMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope)
        try:
            await self.app(scope, receive, send)
        except Exception as exc:
            logging.error(f"Unhandled exception: {exc}", exc_info=True)

            # For user-facing errors, return a friendly message
            response_data = {
                "error": "An unexpected error occurred. Please try again.",
                "detail": "Something went wrong on our end. We've been notified and are looking into it."
            }

            response = JSONResponse(
                status_code=500,
                content=response_data
            )
            await response(scope, receive, send)


def add_error_handlers(app):
    """Add global exception handlers to the application."""

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "status_code": exc.status_code
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        logging.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "An unexpected error occurred",
                "detail": "We apologize for the inconvenience. Our team has been notified."
            }
        )


def setup_logging(log_level: str = "INFO"):
    """
    Set up logging configuration for the application.

    Args:
        log_level: The log level to use (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Create logs directory if it doesn't exist
    import os
    os.makedirs("logs", exist_ok=True)

    # Get the logger
    logger = logging.getLogger()

    # Set the log level
    logger.setLevel(getattr(logging, log_level.upper()))

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create file handler with rotation
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Reduce noise from third-party libraries
    logging.getLogger('sqlalchemy').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)