"""
Purpose:
    Provide the concrete Playwright implementation for the Page interface.

Responsibilities:
    - Wrap Playwright's async Page instance.
    - Implement abstract methods defined in the Page interface.
    - Expose page controls and query methods cleanly.

Must NOT do:
    - Expose internal Playwright page objects to modules calling this class.
    - Contain domain-specific selectors or logic.
"""

from __future__ import annotations
from typing import Any, Optional
from playwright.async_api import Page as PWPage

from app.browser_engine.interfaces.page import Page
from app.browser_engine.interfaces.locator import Locator


class PlaywrightPage(Page):
    """
    Playwright concrete implementation of the Page interface.
    """

    def __init__(self, playwright_page: PWPage) -> None:
        self._page = playwright_page

    async def goto(self, url: str, options: Optional[Any] = None) -> None:
        await self._page.goto(url)

    async def close(self) -> None:
        await self._page.close()

    async def url(self) -> str:
        return self._page.url

    async def title(self) -> str:
        return await self._page.title()

    async def content(self) -> str:
        return await self._page.content()

    async def screenshot(self, options: Optional[Any] = None) -> bytes:
        # Skeleton implementation - returns screenshot bytes
        raise NotImplementedError("To be implemented in a subsequent sprint")

    def locator(self, selector: str) -> Locator:
        # Skeleton implementation
        raise NotImplementedError("To be implemented in a subsequent sprint")

    async def evaluate(self, expression: str, arg: Optional[Any] = None) -> Any:
        return await self._page.evaluate(expression, arg)
