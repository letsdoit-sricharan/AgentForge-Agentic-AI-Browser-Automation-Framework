"""
Centralized logging configuration for AgentForge.

Every module in the application should import the logger
defined here instead of creating its own logger.
"""

from pathlib import Path
import sys

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
)

__all__ = ["logger"]