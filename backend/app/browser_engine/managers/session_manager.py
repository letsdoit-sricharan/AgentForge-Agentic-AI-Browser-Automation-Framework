"""
Purpose:
    High-level manager responsible for controlling a browser session.

Responsibilities:
    - Own a single browser session.
    - Create and track pages.
    - Close all pages before closing the session.
    - Hide browser implementation details.

Must NOT do:
    - Launch browsers.
    - Know about Playwright.
    - Contain business logic.
"""

from __future__ import annotations

from app.browser_engine.interfaces.page import Page
from app.browser_engine.interfaces.session import Session


class SessionManager:
    """
    High-level manager for a browser session.

    A SessionManager owns exactly one browser session and
    manages the lifecycle of all pages created within it.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        """
        Initialize the session manager.

        Args:
            session:
                Browser session implementation.
        """
        self._session = session

        self._pages: list[Page] = []

    async def new_page(self) -> Page:
        """
        Create a new page.

        Returns:
            Page:
                Newly created page.
        """
        page = await self._session.new_page()

        self._pages.append(page)

        return page

    async def close(self) -> None:
        """
        Close all managed pages and then close the session.
        """
        for page in list(self._pages):
            try:
                await page.close()
            except Exception:
                # Ignore page close failures so remaining
                # resources can still be cleaned up.
                pass

        self._pages.clear()

        await self._session.close()

    @property
    def session(self) -> Session:
        """
        Return the underlying browser session.
        """
        return self._session

    @property
    def page_count(self) -> int:
        """
        Return the number of managed pages.
        """
        return len(self._pages)

    @property
    def is_active(self) -> bool:
        """
        Indicates whether the session is active.
        """
        return self._session.is_active