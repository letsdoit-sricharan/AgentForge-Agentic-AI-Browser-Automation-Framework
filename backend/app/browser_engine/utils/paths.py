"""
Purpose:
    Provide utilities for resolving file system paths for download and session storage.

Responsibilities:
    - Return default directories for session profiles, downloads, and screenshots.
    - Ensure directories exist.

Must NOT do:
    - Reference specific local machine hardcoded absolute paths (outside workspace).
"""

from __future__ import annotations
from pathlib import Path

# Resolve base directories relative to the backend app package
APP_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = APP_DIR / "storage"


def get_session_storage_path(session_id: str) -> Path:
    """
    Get the directory path where session state data is stored.
    """
    path = STORAGE_DIR / "sessions" / session_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_download_storage_path() -> Path:
    """
    Get the directory path where downloaded files are saved.
    """
    path = STORAGE_DIR / "downloads"
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_screenshot_storage_path() -> Path:
    """
    Get the directory path where screenshot captures are stored.
    """
    path = STORAGE_DIR / "screenshots"
    path.mkdir(parents=True, exist_ok=True)
    return path
