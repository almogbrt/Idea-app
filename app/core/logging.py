"""Structured JSON logging configuration (structlog).

Cloud Run/Cloud Logging parses JSON written to stdout automatically, so the
production renderer emits one JSON object per line. Local dev uses a
human-readable console renderer instead.

Request-scoped fields (request_id, user_id, conversation_id, agent, tool)
are bound via contextvars so every log line emitted while handling a request
carries them without threading parameters through every call site.
"""

from __future__ import annotations

import logging
import sys
from typing import Any, cast

import structlog
from structlog.contextvars import bind_contextvars, clear_contextvars, unbind_contextvars

from app.core.config import AppEnv, get_settings

__all__ = [
    "configure_logging",
    "get_logger",
    "bind_request_context",
    "clear_request_context",
    "unbind_request_context",
]


def configure_logging() -> None:
    settings = get_settings()

    shared_processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    if settings.app_env == AppEnv.LOCAL:
        renderer: Any = structlog.dev.ConsoleRenderer()
    else:
        renderer = structlog.processors.JSONRenderer()

    structlog.configure(
        processors=[*shared_processors, renderer],
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelNamesMapping().get(settings.log_level.upper(), logging.INFO)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    return cast(structlog.stdlib.BoundLogger, structlog.get_logger(name))


def bind_request_context(**kwargs: Any) -> None:
    bind_contextvars(**kwargs)


def unbind_request_context(*keys: str) -> None:
    unbind_contextvars(*keys)


def clear_request_context() -> None:
    clear_contextvars()
