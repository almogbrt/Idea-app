"""Shared helpers for agent tools that call blocking `googleapiclient` code."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import TypeVar

from googleapiclient.errors import HttpError

from app.core.exceptions import ExternalServiceError
from app.core.logging import get_logger

logger = get_logger(__name__)

T = TypeVar("T")


async def call_google_api(fn: Callable[[], T], *, action: str) -> T:
    """Runs a blocking googleapiclient `.execute()` call off the event loop,
    translating `HttpError` into our `ExternalServiceError`."""
    try:
        return await asyncio.to_thread(fn)
    except HttpError as exc:
        logger.error("google_api_error", action=action, status=exc.status_code, error=str(exc))
        raise ExternalServiceError(f"Google API error during '{action}': {exc.reason}") from exc
