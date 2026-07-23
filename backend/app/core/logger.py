"""
Centralized logging configuration for AgentForge.

Every module in the application should import the logger
defined here instead of creating its own logger.
"""
from __future__ import annotations

import contextvars
import sys
from pathlib import Path

from loguru import logger

from app.core.config import settings

# --------------------------------------------------
# Log Directory
# --------------------------------------------------

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "agentforge.log"

# --------------------------------------------------
# Remove Default Logger
# --------------------------------------------------

logger.remove()

# --------------------------------------------------
# Console Logging
# --------------------------------------------------

logger.add(
    sys.stdout,
    level=settings.LOG_LEVEL,
    colorize=True,
    enqueue=True,
    backtrace=True,
    diagnose=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    ),
)

# --------------------------------------------------
# File Logging
# --------------------------------------------------

logger.add(
    LOG_FILE,
    level=settings.LOG_LEVEL,
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    enqueue=True,
    backtrace=True,
    diagnose=False,
    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level} | "
        "{name}:{function}:{line} | "
        "{message}"
    ),
    serialize=True, # Structured JSON logging
)

# --------------------------------------------------
# Contextual Timelines
# --------------------------------------------------
session_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("session_id", default="unknown")
step_name_var: contextvars.ContextVar[str] = contextvars.ContextVar("step_name", default="unknown")

def contextual_logger():
    """Returns a logger bound with the current session and step context."""
    return logger.bind(session_id=session_id_var.get(), step_name=step_name_var.get())

__all__ = ["logger", "contextual_logger", "session_id_var", "step_name_var"]
