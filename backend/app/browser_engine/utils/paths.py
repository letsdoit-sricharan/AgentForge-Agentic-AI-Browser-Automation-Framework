"""
Purpose:
    Provides filesystem path utilities for the Browser Engine.

Responsibilities:
    - Manage browser engine directories.
    - Ensure required folders exist.
    - Generate common file paths.

Must NOT do:
    - Perform browser automation.
    - Read or write cookies.
    - Handle downloads.
"""

from __future__ import annotations

from pathlib import Path


class PathManager:
    """
    Utility class for managing browser engine paths.
    """

    _ROOT = Path.cwd()

    _SCREENSHOTS = _ROOT / "screenshots"
    _DOWNLOADS = _ROOT / "downloads"
    _COOKIES = _ROOT / "cookies"
    _TEMP = _ROOT / "temp"

    @classmethod
    def ensure_directories(cls) -> None:
        """
        Create required directories if they do not exist.
        """
        for directory in (
            cls._SCREENSHOTS,
            cls._DOWNLOADS,
            cls._COOKIES,
            cls._TEMP,
        ):
            directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def screenshot_path(cls, filename: str) -> Path:
        cls.ensure_directories()
        return cls._SCREENSHOTS / filename

    @classmethod
    def download_path(cls, filename: str) -> Path:
        cls.ensure_directories()
        return cls._DOWNLOADS / filename

    @classmethod
    def cookie_path(cls, filename: str = "cookies.json") -> Path:
        cls.ensure_directories()
        return cls._COOKIES / filename

    @classmethod
    def temp_path(cls, filename: str) -> Path:
        cls.ensure_directories()
        return cls._TEMP / filename