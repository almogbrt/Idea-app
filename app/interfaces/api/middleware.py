"""Request-scoped middleware: correlation IDs + structured access logging."""

from __future__ import annotations

import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import bind_request_context, clear_request_context, get_logger

logger = get_logger(__name__)


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
        request.state.request_id = request_id
        bind_request_context(request_id=request_id)

        started = time.monotonic()
        try:
            response = await call_next(request)
        finally:
            clear_request_context()

        duration_ms = int((time.monotonic() - started) * 1000)
        logger.info(
            "http_request",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
            request_id=request_id,
        )
        response.headers["x-request-id"] = request_id
        return response
