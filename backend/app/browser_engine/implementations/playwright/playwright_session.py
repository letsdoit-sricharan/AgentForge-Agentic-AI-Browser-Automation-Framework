"""
Purpose:
    Provide the concrete Playwright implementation for the Session interface.

Responsibilities:
    - Wrap Playwright's async BrowserContext instance.
    - Implement abstract methods defined in the Session interface.
    - Manage active pages/tabs and storage state within the context.

Must NOT do:
    - Expose internal Playwright BrowserContext objects to modules calling this class.
    - Access/read/write configuration files directly.
"""

from __future__ import annotations
from typing import Any, List, Dict, TYPE_CHECKING
from playwright.async_api import BrowserContext as PWBrowserContext

from app.browser_engine.interfaces.session import Session

if TYPE_CHECKING:
    from app.browser_engine.interfaces.page import Page


class PlaywrightSession(Session):
    """
    Playwright concrete implementation of the Session interface.
    """

    def __init__(self, playwright_context: PWBrowserContext) -> None:
        self._context = playwright_context
        self._pages: List[Page] = []

    async def new_page(self) -> Page:
        # Skeleton implementation
        raise NotImplementedError("To be implemented in a subsequent sprint")

    async def close(self) -> None:
        await self._context.close()

    @property
    def pages(self) -> List[Page]:
        return self._pages

    async def get_cookies(self) -> List[Dict[str, Any]]:
        return await self._context.cookies()

    async def add_cookies(self, cookies: List[Dict[str, Any]]) -> None:
        await self._context.add_cookies(cookies)

    async def clear_cookies(self) -> None:
        await self._context.clear_cookies()

    async def get_storage_state(self) -> Dict[str, Any]:
        return await self._context.storage_state()
