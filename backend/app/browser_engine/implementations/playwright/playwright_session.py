"""
Purpose:
    Playwright implementation of the Session interface.

Responsibilities:
    - Manage a single Playwright BrowserContext.
    - Create browser pages within the context.
    - Close the browser context.
    - Expose the session state.

Must NOT do:
    - Expose Playwright objects outside the Browser Engine.
    - Launch or close the browser process.
    - Perform page interactions.
    - Handle logging or retries.
"""

from __future__ import annotations

from playwright.async_api import BrowserContext

from app.browser_engine.interfaces.page import Page
from app.browser_engine.interfaces.session import Session
from app.browser_engine.implementations.playwright.playwright_page import (
    PlaywrightPage,
)


class PlaywrightSession(Session):
    """
    Playwright implementation of the Session interface.

    A session wraps a Playwright BrowserContext, providing
    isolated browser state such as cookies, local storage,
    authentication, and multiple pages.
    """

    def __init__(self, context: BrowserContext) -> None:
        """
        Initialize a Playwright browser session.

        Args:
            context:
                The underlying Playwright BrowserContext.
        """
        self._context = context
        self._closed = False

    async def new_page(self) -> Page:
        """
        Create a new page within this session.

        Returns:
            A Browser Engine Page abstraction.
        """
        playwright_page = await self._context.new_page()
        return PlaywrightPage(playwright_page)

    async def close(self) -> None:
        """
        Close the browser session and release its resources.
        """
        if self._closed:
            return

        await self._context.close()
        self._closed = True

    @property
    def is_active(self) -> bool:
        """
        Indicates whether the session is currently active.

        Returns:
            True if the session has not been closed.
        """
        return not self._closed