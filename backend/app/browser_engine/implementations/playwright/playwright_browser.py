"""
Purpose:
    Provide the concrete Playwright implementation for the Browser interface.

Responsibilities:
    - Wrap Playwright's async Browser instance.
    - Implement abstract methods defined in the Browser interface.
    - Manage the lifetime of the underlying Playwright Browser process.

Must NOT do:
    - Expose internal Playwright browser objects to modules calling this class.
    - Contain domain-specific logic or website-specific details.
"""

from __future__ import annotations
from typing import List, Optional, Any, TYPE_CHECKING
from playwright.async_api import Browser as PWBrowser

from app.browser_engine.interfaces.browser import Browser

if TYPE_CHECKING:
    from app.browser_engine.interfaces.session import Session


class PlaywrightBrowser(Browser):
    """
    Playwright concrete implementation of the Browser interface.
    """

    def __init__(self, playwright_browser: PWBrowser) -> None:
        self._browser = playwright_browser
        self._sessions: List[Session] = []

    async def new_session(self, options: Optional[Any] = None) -> Session:
        # Skeleton implementation
        raise NotImplementedError("To be implemented in a subsequent sprint")

    async def close(self) -> None:
        await self._browser.close()

    def is_connected(self) -> bool:
        return self._browser.is_connected()

    @property
    def sessions(self) -> List[Session]:
        return self._sessions
