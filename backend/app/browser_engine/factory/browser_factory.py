"""
Purpose:
    Provide a factory for creating instances of Browser and Session interfaces.

Responsibilities:
    - Instantiate the concrete Browser class based on settings (e.g. Playwright or future adapters).
    - Provide a centralized configuration point for selecting the underlying automation library.

Must NOT do:
    - Couple client code directly to concrete classes.
    - Leak Playwright imports to the rest of the application (use dynamic imports or adapter packaging).
"""

from __future__ import annotations
from typing import Any, Optional

from app.browser_engine.interfaces.browser import Browser


class BrowserFactory:
    """
    Factory for producing concrete instances of the Browser interface.
    """

    @staticmethod
    async def create_browser(engine_type: str = "playwright", options: Optional[Any] = None) -> Browser:
        """
        Create and launch a concrete Browser instance.

        Args:
            engine_type: The automation engine backend to use ('playwright', 'selenium', etc.).
            options: Configuration options for launching the browser.

        Returns:
            An instance of the Browser interface.
        """
        if engine_type.lower() == "playwright":
            from app.browser_engine.implementations.playwright.playwright_adapter import PlaywrightAdapter
            adapter = PlaywrightAdapter()
            return await adapter.launch(options)
        else:
            raise ValueError(f"Unsupported browser engine type: {engine_type}")
