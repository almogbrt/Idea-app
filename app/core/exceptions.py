"""Application-wide exception hierarchy and FastAPI error handlers.

Every exception raised by domain/application/infrastructure code should be
(or wrap into) an `AppError` subclass so the API layer can map it to a
consistent JSON error body without each route needing its own try/except.
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.logging import get_logger

logger = get_logger(__name__)


class AppError(Exception):
    """Base class for all application errors."""

    error_code: str = "internal_error"
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class NotFoundError(AppError):
    error_code = "not_found"
    status_code = status.HTTP_404_NOT_FOUND


class ValidationError(AppError):
    error_code = "validation_error"
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT


class AuthError(AppError):
    error_code = "auth_error"
    status_code = status.HTTP_401_UNAUTHORIZED


class ForbiddenError(AppError):
    error_code = "forbidden"
    status_code = status.HTTP_403_FORBIDDEN


class RateLimitError(AppError):
    error_code = "rate_limited"
    status_code = status.HTTP_429_TOO_MANY_REQUESTS


class ExternalServiceError(AppError):
    """Raised when a downstream dependency (Google API, LLM provider, etc.) fails."""

    error_code = "external_service_error"
    status_code = status.HTTP_502_BAD_GATEWAY


class ConflictError(AppError):
    error_code = "conflict"
    status_code = status.HTTP_409_CONFLICT


def _request_id(request: Request) -> str | None:
    return getattr(request.state, "request_id", None)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
        logger.warning(
            "app_error",
            error_code=exc.error_code,
            message=exc.message,
            details=exc.details,
            path=request.url.path,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error_code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
                "request_id": _request_id(request),
            },
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        logger.error(
            "unhandled_exception",
            exc_info=exc,
            path=request.url.path,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error_code": "internal_error",
                "message": "An unexpected error occurred.",
                "details": {},
                "request_id": _request_id(request),
            },
        )
