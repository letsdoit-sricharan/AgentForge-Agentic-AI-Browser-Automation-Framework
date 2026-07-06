"""
Purpose:
    Owns the Playwright runtime for the Browser Engine.

Responsibilities:
    - Start and stop the Playwright runtime.
    - Launch browser instances.
    - Hide Playwright initialization from the rest of the implementation layer.

Must NOT do:
    - Open pages.
    - Navigate websites.
    - Perform browser actions.
    - Contain business logic.
"""

from __future__ import annotations

from playwright.async_api import (
    Browser as PlaywrightBrowserInstance,
    Playwright,
    async_playwright,
)

from app.browser_engine.exceptions.browser_errors import (
    BrowserClosedError,
    BrowserLaunchError,
)
from app.browser_engine.models.browser_options import BrowserOptions


class PlaywrightAdapter:
    """
    Manages the lifecycle of the Playwright runtime.

    This class is the only component responsible for interacting with
    `async_playwright()`.
    """

    def __init__(self) -> None:
        self._playwright: Playwright | None = None

    async def start(self) -> None:
        """
        Start the Playwright runtime.

        Raises:
            BrowserLaunchError:
                If Playwright fails to start.
        """
        if self._playwright is not None:
            return

        try:
            self._playwright = await async_playwright().start()
        except Exception as exc:
            raise BrowserLaunchError(
                "Failed to start Playwright runtime."
            ) from exc

    async def stop(self) -> None:
        """
        Stop the Playwright runtime.
        """
        if self._playwright is None:
            return

        await self._playwright.stop()
        self._playwright = None

    async def launch_browser(
        self,
        options: BrowserOptions,
    ) -> PlaywrightBrowserInstance:
        """
        Launch a Chromium browser.

        Args:
            options:
                Browser launch configuration.

        Returns:
            Native Playwright Browser instance.

        Raises:
            BrowserClosedError:
                If the Playwright runtime has not been started.

            BrowserLaunchError:
                If the browser fails to launch.
        """

        if self._playwright is None:
            raise BrowserClosedError(
                "Playwright runtime has not been started."
            )

        try:
            browser = await self._playwright.chromium.launch(
                headless=options.headless,
                slow_mo=options.slow_mo,
            )

            return browser

        except Exception as exc:
            raise BrowserLaunchError(
                "Failed to launch Chromium."
            ) from exc