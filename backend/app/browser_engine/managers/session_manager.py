"""
Purpose:
    High-level manager responsible for controlling a browser session.

Responsibilities:
    - Own a browser session.
    - Create and track pages.
    - Clean up pages.
    - Notify BrowserManager when closed.

Must NOT:
    - Launch browsers.
    - Know about Playwright.
    - Know about BrowserManager.
"""

from __future__ import annotations

import uuid
from collections.abc import Callable

from app.browser_engine.interfaces.page import Page
from app.browser_engine.interfaces.session import Session


class SessionManager:
    """
    High-level manager for a browser session.
    """

    def __init__(
        self,
        session: Session,
        on_close: Callable[[str], None] | None = None,
    ) -> None:

        self._id = str(uuid.uuid4())

        self._session = session

        self._pages: dict[str, Page] = {}

        self._on_close = on_close

    async def new_page(self) -> Page:
        """
        Create a new page.
        """
        page = await self._session.new_page()

        page_id = str(uuid.uuid4())

        self._pages[page_id] = page

        return page

    async def close(self) -> None:
        """
        Close all pages and the session.
        """
        pages = list(self._pages.values())

        for page in pages:
            try:
                await page.close()
            except Exception:
                pass

        self._pages.clear()

        await self._session.close()

        if self._on_close is not None:
            self._on_close(self._id)

    @property
    def id(self) -> str:
        """
        Session identifier.
        """
        return self._id

    @property
    def session(self) -> Session:
        """
        Underlying browser session.
        """
        return self._session

    @property
    def page_count(self) -> int:
        """
        Number of active pages.
        """
        return len(self._pages)

    @property
    def pages(self) -> tuple[Page, ...]:
        """
        Immutable view of active pages.
        """
        return tuple(self._pages.values())

    @property
    def is_active(self) -> bool:
        """
        Whether the session is active.
        """
        return self._session.is_active