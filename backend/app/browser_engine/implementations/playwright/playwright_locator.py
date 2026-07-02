"""
Purpose:
    Provide the concrete Playwright implementation for the Locator interface.

Responsibilities:
    - Wrap Playwright's async Locator instance.
    - Implement abstract methods defined in the Locator interface.
    - Route interactions (click, fill, checks) and state checks to Playwright.

Must NOT do:
    - Expose internal Playwright Locator objects to modules calling this class.
"""

from __future__ import annotations
from typing import Any, Optional
from playwright.async_api import Locator as PWLocator

from app.browser_engine.interfaces.locator import Locator


class PlaywrightLocator(Locator):
    """
    Playwright concrete implementation of the Locator interface.
    """

    def __init__(self, playwright_locator: PWLocator) -> None:
        self._locator = playwright_locator

    async def click(self, options: Optional[Any] = None) -> None:
        await self._locator.click()

    async def fill(self, value: str, options: Optional[Any] = None) -> None:
        await self._locator.fill(value)

    async def hover(self, options: Optional[Any] = None) -> None:
        await self._locator.hover()

    async def check(self, options: Optional[Any] = None) -> None:
        await self._locator.check()

    async def uncheck(self, options: Optional[Any] = None) -> None:
        await self._locator.uncheck()

    async def text_content(self) -> Optional[str]:
        return await self._locator.text_content()

    async def inner_text(self) -> str:
        return await self._locator.inner_text()

    async def get_attribute(self, name: str) -> Optional[str]:
        return await self._locator.get_attribute(name)

    async def is_visible(self) -> bool:
        return await self._locator.is_visible()

    async def is_enabled(self) -> bool:
        return await self._locator.is_enabled()

    async def wait_for(self, state: Optional[str] = None, timeout: Optional[float] = None) -> None:
        # Skeleton implementation mapping state options to PW locator wait_for
        raise NotImplementedError("To be implemented in a subsequent sprint")

    async def count(self) -> int:
        return await self._locator.count()

    def nth(self, index: int) -> Locator:
        return PlaywrightLocator(self._locator.nth(index))
