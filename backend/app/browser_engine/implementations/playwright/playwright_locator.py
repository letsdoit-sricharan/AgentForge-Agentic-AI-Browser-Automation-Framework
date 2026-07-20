"""
Purpose:
    Playwright implementation of the Locator interface.

Responsibilities:
    - Perform element-level interactions.
    - Hide the native Playwright Locator object.
    - Translate Playwright exceptions into AgentForge exceptions.

Must NOT do:
    - Launch browsers.
    - Manage browser sessions.
    - Perform page navigation.
    - Contain business logic.
"""

from __future__ import annotations

from playwright.async_api import (
    Locator as PlaywrightLocatorInstance,
    TimeoutError as PlaywrightTimeoutError,
)

from app.browser_engine.exceptions.browser_errors import LocatorError
from app.browser_engine.exceptions.timeout_errors import (
    BrowserTimeoutError,
)
from app.browser_engine.interfaces.locator import Locator


class PlaywrightLocator(Locator):
    """
    Playwright implementation of the Locator interface.
    """

    def __init__(
        self,
        locator: PlaywrightLocatorInstance,
    ) -> None:
        """
        Initialize the locator.

        Args:
            locator:
                Native Playwright Locator.
        """
        self._locator = locator

    async def click(self) -> None:
        """
        Click the element.
        """
        try:
            await self._locator.click()

        except PlaywrightTimeoutError as exc:
            raise BrowserTimeoutError(
                "Timed out while clicking the element."
            ) from exc

        except Exception as exc:
            raise LocatorError(
                "Failed to click the element."
            ) from exc

    async def fill(self, value: str) -> None:
        """
        Fill the element with the given value.
        """
        try:
            await self._locator.fill(value)

        except PlaywrightTimeoutError as exc:
            raise BrowserTimeoutError(
                "Timed out while filling the element."
            ) from exc

        except Exception as exc:
            raise LocatorError(
                "Failed to fill the element."
            ) from exc

    async def text(self) -> str:
        """
        Return the visible text of the element.
        """
        try:
            return await self._locator.inner_text()

        except PlaywrightTimeoutError as exc:
            raise BrowserTimeoutError(
                "Timed out while retrieving element text."
            ) from exc

        except Exception as exc:
            raise LocatorError(
                "Failed to retrieve element text."
            ) from exc

    async def is_visible(self) -> bool:
        """
        Check whether the element is visible.
        """
        try:
            return await self._locator.is_visible()

        except Exception as exc:
            raise LocatorError(
                "Failed to determine element visibility."
            ) from exc

    async def hover(self) -> None:
        """
        Hover over the element.
        """
        try:
            await self._locator.hover()

        except PlaywrightTimeoutError as exc:
            raise BrowserTimeoutError(
                "Timed out while hovering over the element."
            ) from exc

        except Exception as exc:
            raise LocatorError(
                "Failed to hover over the element."
            ) from exc

    async def select(self, value: str) -> None:
        """
        Select an option from a dropdown.
        """
        try:
            await self._locator.select_option(value)

        except PlaywrightTimeoutError as exc:
            raise BrowserTimeoutError(
                "Timed out while selecting an option."
            ) from exc

        except Exception as exc:
            raise LocatorError(
                "Failed to select an option."
            ) from exc

    async def wait(
        self,
        timeout: int | None = None,
    ) -> None:
        """
        Wait until the element becomes visible.
        """
        try:
            await self._locator.wait_for(
                state="visible",
                timeout=timeout,
            )

        except PlaywrightTimeoutError as exc:
            raise BrowserTimeoutError(
                "Timed out while waiting for the element."
            ) from exc

        except Exception as exc:
            raise LocatorError(
                "Failed while waiting for the element."
            ) from exc

    async def wait_until_hidden(
        self,
        timeout: int | None = None,
    ) -> None:
        """
        Wait until the element becomes hidden.
        """
        try:
            await self._locator.wait_for(
                state="hidden",
                timeout=timeout,
            )

        except PlaywrightTimeoutError as exc:
            raise BrowserTimeoutError(
                "Timed out while waiting for the element to become hidden."
            ) from exc

        except Exception as exc:
            raise LocatorError(
                "Failed while waiting for the element to become hidden."
            ) from exc

    async def scroll_into_view(self) -> None:
        """
        Scroll the element into the visible viewport.
        """
        try:
            await self._locator.scroll_into_view_if_needed()

        except PlaywrightTimeoutError as exc:
            raise BrowserTimeoutError(
                "Timed out while scrolling the element into view."
            ) from exc

        except Exception as exc:
            raise LocatorError(
                "Failed to scroll the element into view."
            ) from exc
    
    def first(self) -> Locator:
        """
        Return the first matching element.
        """
        return PlaywrightLocator(
            self._locator.first
        )

    def last(self) -> Locator:
        """
        Return the last matching element.
        """
        return PlaywrightLocator(
            self._locator.last
        )

    def nth(self, index: int) -> Locator:
        """
        Return the nth matching element.
        """
        return PlaywrightLocator(
            self._locator.nth(index)
        )