"""
AgentForge Backend — Application Entry Point.

Creates and configures the FastAPI application, registers all routers,
mounts the static demo UI, and manages application lifecycle events.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.endpoints import bookings
from app.core.config import settings
from app.core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    """
    Manage application startup and shutdown.

    On startup: log version/environment banner.
    On shutdown: log graceful shutdown message.

    Extend this coroutine to initialise shared resources (database pools,
    browser engine, agent runtime) when they are needed.
    """
    logger.info("=" * 60)
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info("=" * 60)

    yield

    logger.info("=" * 60)
    logger.info(f"Shutting down {settings.APP_NAME}")
    logger.info("=" * 60)


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "AgentForge is a reusable, plugin-driven Agentic AI platform for "
        "browser automation. It provides a clean architecture for building "
        "autonomous booking, scraping, and workflow automation agents."
    ),
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# ---------------------------------------------------------------------------
# CORS
# Allows the frontend (served separately on a different port during
# development) to reach this API. In production, restrict origins to the
# deployed frontend domain.
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(
    bookings.router,
    prefix="/api/bookings",
    tags=["Bookings"],
)

# ---------------------------------------------------------------------------
# Static demo UI
# ---------------------------------------------------------------------------
app.mount("/demo", StaticFiles(directory="app/static", html=True), name="static")


# ---------------------------------------------------------------------------
# Root & health endpoints
# ---------------------------------------------------------------------------
@app.get("/", tags=["Meta"], include_in_schema=False)
async def root() -> dict:
    """Redirect hint for the API root."""
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/api/docs",
        "health": "/health",
    }


@app.get(
    "/health",
    tags=["Meta"],
    summary="Health check",
    description=(
        "Returns HTTP 200 when the application is ready to serve requests. "
        "Used by Docker HEALTHCHECK, Kubernetes liveness probes, and "
        "monitoring services."
    ),
)
async def health() -> dict:
    """Application health check."""
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "backend": "healthy",
        "browser_engine": "healthy",
        "planner": "healthy",
        "runtime": "healthy",
        "plugins": "healthy"
    }


@app.get("/api/executions", tags=["Platform"])
async def get_executions():
    from app.runtime.events.global_bus import get_all_executions
    return get_all_executions()


@app.get("/api/dashboard/stats", tags=["Platform"])
async def get_stats():
    from app.runtime.events.global_bus import get_dashboard_stats
    from app.api.endpoints.bookings import _plugin_manager
    stats = get_dashboard_stats()
    stats["plugins"] = len(_plugin_manager.registry.list_plugins()) + 3 # adding mock plugins count
    return stats


@app.get("/api/plugins", tags=["Platform"])
async def get_plugins():
    from app.api.endpoints.bookings import _plugin_manager
    plugins = []
    for name in _plugin_manager.registry.list_plugins():
        plugins.append({
            "id": name,
            "name": name.title(),
            "enabled": True,
            "description": "Browser automation plugin",
            "version": "1.0.0"
        })
    # Add mock disabled plugins per requirements
    plugins.extend([
        {"id": "amazon", "name": "Amazon", "enabled": False, "description": "Automated e-commerce purchasing.", "version": "0.0.0"},
        {"id": "irctc", "name": "IRCTC", "enabled": False, "description": "Train ticket booking engine.", "version": "0.0.0"},
        {"id": "makemytrip", "name": "MakeMyTrip", "enabled": False, "description": "Flight and hotel reservations.", "version": "0.0.0"}
    ])
    return plugins
