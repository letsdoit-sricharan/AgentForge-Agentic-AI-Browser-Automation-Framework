"""
Main entry point for the AgentForge backend.

This module creates and configures the FastAPI application.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.logger import logger
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import bookings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    """

    logger.info("=" * 60)
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info("=" * 60)

    # Future initialization:
    # - Database connection
    # - Browser engine
    # - Agent runtime
    # - Plugin registry

    yield

    logger.info("=" * 60)
    logger.info(f"Shutting down {settings.APP_NAME}")
    logger.info("=" * 60)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Reusable Agentic AI Platform",
    lifespan=lifespan,
)


app.include_router(bookings.router, prefix="/api/bookings", tags=["Bookings"])
app.mount("/demo", StaticFiles(directory="app/static", html=True), name="static")

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint.
    """
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "message": "AgentForge Backend is running"
    }


@app.get("/health", tags=["Health"])
async def health():
    """
    Health check endpoint.

    Used by deployment platforms, Docker,
    Kubernetes, and monitoring services.
    """
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }