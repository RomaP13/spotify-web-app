"""Logging Middleware for FastAPI."""

import time

from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.types import ASGIApp

from app.api.utils.logging_utils import LogMessageEmojis


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests and responses."""

    def __init__(self, app: ASGIApp) -> None:
        """Initializes the LoggingMiddleware instance."""
        super().__init__(app)
        self._emojis = LogMessageEmojis()

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Logs the request and response for a given FastAPI request."""
        start_time = time.time()

        # Read request body
        try:
            body = await request.body()
            body_text = body.decode("utf-8") if body else "    No Body"
        except Exception as e:
            body_text = f"Error reading body: {e}"

        # Format headers for readability
        headers_str = "\n".join(
            f"        {k}: {v}" for k, v in request.headers.items()
        )

        # Log request
        logger.info(
            f"\n{self._emojis.get_emoji('incoming_request')} Incoming Request:\n"
            f"   {self._emojis.get_emoji('request_method')} {request.method} {request.url}\n"
            f"   {self._emojis.get_emoji('request_headers')} Headers:\n{headers_str}\n"
            f"   {self._emojis.get_emoji('request_body')} Body:\n    {body_text}\n"
        )

        response: Response = await call_next(request)

        process_time = time.time() - start_time

        # Log response
        logger.info(
            f"\n{self._emojis.get_emoji('response')} Response:\n"
            f"   {self._emojis.get_response_status_emoji(response.status_code)} Status: {response.status_code}\n"
            f"   {self._emojis.get_emoji('process_time')} Process Time: {process_time:.2f}s\n"
        )

        return response
