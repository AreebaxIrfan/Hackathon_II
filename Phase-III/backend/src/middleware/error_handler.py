"""
Error handling middleware for the Chat Flow API
"""
import logging
from typing import Callable, Awaitable
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException


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