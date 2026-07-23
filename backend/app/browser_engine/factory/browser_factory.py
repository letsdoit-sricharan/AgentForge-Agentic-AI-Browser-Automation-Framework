"""
Purpose:
    Factory responsible for creating Browser Engine implementations.

Responsibilities:
    - Instantiate browser implementations.
    - Hide browser backend details.
    - Return Browser interface objects.

Must NOT do:
    - Launch browsers.
    - Manage browser lifecycle.
    - Store browser instances.
    - Contain business logic.
"""

from __future__ import annotations

from app.browser_engine.implementations.playwright.playwright_adapter import (
    PlaywrightAdapter,
)
from app.browser_engine.implementations.playwright.playwright_browser import (
    PlaywrightBrowser,
)
from app.browser_engine.interfaces.browser import Browser


class BrowserFactory:
    """
    Factory responsible for creating Browser implementations.
    """

    @staticmethod
    def create_browser() -> Browser:
        """
        Create a browser implementation.

        Returns:
            Browser:
                A browser implementing the Browser interface.
        """
        adapter = PlaywrightAdapter()

        return PlaywrightBrowser(adapter)
