"""
Purpose:
    Utility functions for storing and loading browser cookies.

Responsibilities:
    - Save cookies to disk.
    - Load cookies from disk.

Must NOT do:
    - Manage browser sessions.
    - Depend on Playwright.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class CookieManager:
    """
    Utility class for cookie persistence.
    """

    @staticmethod
    def save(
        cookies: list[dict[str, Any]],
        path: Path,
    ) -> None:
        """
        Save cookies to a JSON file.
        """
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(cookies, file, indent=4)

    @staticmethod
    def load(path: Path) -> list[dict[str, Any]]:
        """
        Load cookies from a JSON file.
        """
        if not path.exists():
            return []

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)
