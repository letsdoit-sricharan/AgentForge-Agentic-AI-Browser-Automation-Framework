"""
Purpose:
    Playwright implementation of the Session interface.

Responsibilities:
    - Manage a browser session (BrowserContext).
    - Create pages.
    - Close the session.
    - Hide Playwright BrowserContext from the rest of AgentForge.

Must NOT do:
    - Launch browsers.
    - Manage the Playwright runtime.
    - Perform page interactions.
    - Contain business logic.
"""

from __future__ import annotations

from playwright.async_api import BrowserContext

from app.browser_engine.exceptions.browser_errors import SessionError
from app.browser_engine.implementations.playwright.playwright_page import (
    PlaywrightPage,
)
from app.browser_engine.interfaces.page import Page
from app.browser_engine.interfaces.session import Session


class PlaywrightSession(Session):
    """
    Playwright implementation of the Session interface.
    """

    def __init__(self, context: BrowserContext) -> None:
        """
        Initialize the session.

        Args:
            context:
                Native Playwright BrowserContext.
        """
        self._context = context

    async def new_page(self) -> Page:
        """
        Create a new page within the current browser session.

        Returns:
            A Page implementation.

        Raises:
            SessionError:
                If page creation fails.
        """
        try:
            page = await self._context.new_page()
            return PlaywrightPage(page)

        except Exception as exc:
            raise SessionError(
                "Failed to create a new page."
            ) from exc

    async def close(self) -> None:
        """
        Close the browser session.
        """
        try:
            await self._context.close()

        except Exception as exc:
            raise SessionError(
                "Failed to close the browser session."
            ) from exc

    @property
    def is_closed(self) -> bool:
        """
        Indicates whether the session has been closed.

        Returns:
            True if the underlying BrowserContext is closed,
            otherwise False.
        """
        try:
            return self._context.pages is None
        except Exception:
            return True