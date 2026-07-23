"""
Purpose:
    Utility functions for downloaded files.

Responsibilities:
    - Save downloaded files.
    - Generate unique filenames.
    - Move downloads.

Must NOT do:
    - Launch browsers.
    - Manage Playwright downloads directly.
"""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from app.browser_engine.utils.paths import PathManager


class DownloadManager:
    """
    Utility class for managing downloaded files.
    """

    @staticmethod
    def generate_filename(prefix: str, extension: str) -> str:
        """
        Generate a timestamp-based filename.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        extension = extension.lstrip(".")
        return f"{prefix}_{timestamp}.{extension}"

    @staticmethod
    def move(source: Path, destination: Path) -> Path:
        """
        Move a file to a destination.
        """
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))
        return destination

    @staticmethod
    def default_download_path(filename: str) -> Path:
        """
        Return the default download location.
        """
        return PathManager.download_path(filename)
