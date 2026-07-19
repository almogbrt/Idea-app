"""FastAPI application factory — the composition root's entry point.

Run locally with: uvicorn app.main:app --reload
Run in Cloud Run: uvicorn app.main:app --host 0.0.0.0 --port $PORT
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import get_settings
from app.core.container import Container
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging, get_logger
from app.interfaces.api.middleware import RequestContextMiddleware
from app.interfaces.api.v1 import auth as auth_router
from app.interfaces.api.v1 import calendar as calendar_router
from app.interfaces.api.v1 import chat as chat_router
from app.interfaces.api.v1 import files as files_router
from app.interfaces.api.v1 import health as health_router
from app.interfaces.api.v1 import internal as internal_router
from app.interfaces.api.v1 import workspace as workspace_router

_WEB_DIR = Path(__file__).parent / "interfaces" / "web"

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    container = Container(settings)
    container.bootstrap_agents()
    app.state.container = container
    logger.info("app_started", env=settings.app_env.value)
    yield
    await container.shutdown()
    logger.info("app_stopped")


def create_app() -> FastAPI:
    configure_logging()
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description="Edith — a business operating system, not a chatbot.",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(RequestContextMiddleware)
    register_exception_handlers(app)

    app.include_router(health_router.router, prefix="/api/v1")
    app.include_router(auth_router.router, prefix="/api/v1")
    app.include_router(chat_router.router, prefix="/api/v1")
    app.include_router(workspace_router.router, prefix="/api/v1")
    app.include_router(internal_router.router, prefix="/api/v1")
    app.include_router(calendar_router.router, prefix="/api/v1")
    app.include_router(files_router.router, prefix="/api/v1")

    app.mount("/static", StaticFiles(directory=str(_WEB_DIR / "static")), name="static")
    templates = Jinja2Templates(directory=str(_WEB_DIR / "templates"))

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def chat_ui(request: Request) -> HTMLResponse:
        return templates.TemplateResponse(request, "index.html", {})

    @app.get("/sw.js", include_in_schema=False)
    async def service_worker() -> FileResponse:
        # Served from the root path (not /static/sw.js) so its default scope
        # covers the whole app — required for install/"add to home screen".
        return FileResponse(_WEB_DIR / "static" / "sw.js", media_type="application/javascript")

    return app


app = create_app()
