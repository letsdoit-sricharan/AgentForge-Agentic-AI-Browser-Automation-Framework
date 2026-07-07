"""
Purpose:
    Playwright implementation of the Page interface.

Responsibilities:
    - Perform page-level browser operations.
    - Hide the Playwright Page object.
    - Translate Playwright exceptions into AgentForge exceptions.

Must NOT do:
    - Launch browsers.
    - Manage browser sessions.
    - Contain business logic.
"""

from __future__ import annotations
from pathlib import Path

from playwright.async_api import (
    Page as PlaywrightPageInstance,
    TimeoutError as PlaywrightTimeoutError,
)

from app.browser_engine.exceptions.browser_errors import PageError
from app.browser_engine.exceptions.navigation_errors import NavigationError
from app.browser_engine.exceptions.timeout_errors import BrowserTimeoutError
from app.browser_engine.implementations.playwright.playwright_locator import (
    PlaywrightLocator,
)
from app.browser_engine.interfaces.locator import Locator
from app.browser_engine.interfaces.page import Page
from app.browser_engine.models.load_state import LoadState
from app.browser_engine.models.navigation_options import NavigationOptions
from app.browser_engine.models.screenshot_options import ScreenshotOptions


class PlaywrightPage(Page):
    """
    Playwright implementation of the Page interface.
    """

    def __init__(self, page: PlaywrightPageInstance) -> None:
        self._page = page

    async def goto(
        self,
        url: str,
        options: NavigationOptions | None = None,
    ) -> None:
        """
        Navigate to a URL.
        """
        try:
            kwargs = {}

            if options is not None:
                kwargs["wait_until"] = options.wait_until.value
                kwargs["timeout"] = options.timeout

            await self._page.goto(url, **kwargs)

        except PlaywrightTimeoutError as exc:
            raise BrowserTimeoutError(
                f"Navigation to '{url}' timed out."
            ) from exc

        except Exception as exc:
            raise NavigationError(
                f"Failed to navigate to '{url}'."
            ) from exc

    async def title(self) -> str:
        """
        Return the current page title.
        """
        try:
            return await self._page.title()

        except Exception as exc:
            raise PageError(
                "Failed to retrieve page title."
            ) from exc

    @property
    def url(self) -> str:
        """
        Return the current page URL.
        """
        return self._page.url

    def locator(self, selector: str) -> Locator:
        """
        Create a locator for the given selector.
        """
        return PlaywrightLocator(
            self._page.locator(selector)
        )

    async def screenshot(
        self,
        options: ScreenshotOptions,
    ) -> Path:
        """
        Capture a screenshot of the current page.

        Returns:
            Path to the saved screenshot.
        """
        try:
            await self._page.screenshot(
                path=str(options.path),
                full_page=options.full_page,
                type=options.image_type.value,
                quality=options.quality,
            )

            return options.path

        except Exception as exc:
            raise PageError(
                "Failed to capture screenshot."
            ) from exc

    async def wait_for_load(
        self,
        state: LoadState = LoadState.LOAD,
        timeout: int | None = None,
    ) -> None:
        """
        Wait until the page reaches the specified load state.
        """
        try:
            await self._page.wait_for_load_state(
                state=state.value,
                timeout=timeout,
            )

        except PlaywrightTimeoutError as exc:
            raise BrowserTimeoutError(
                "Timed out while waiting for page load."
            ) from exc

    async def close(self) -> None:
        """
        Close the page.
        """
        try:
            await self._page.close()

        except Exception as exc:
            raise PageError(
                "Failed to close page."
            ) from exc

    async def reload(self) -> None:
        """
        Reload the current page.

        Note:
            This is an implementation convenience method and is
            not currently part of the Page interface.
        """
        try:
            await self._page.reload()

        except PlaywrightTimeoutError as exc:
            raise BrowserTimeoutError(
                "Page reload timed out."
            ) from exc

        except Exception as exc:
            raise PageError(
                "Failed to reload page."
            ) from exc