"""
Purpose:
    High-level manager responsible for controlling the browser runtime.

Responsibilities:
    - Own a single browser instance.
    - Launch and stop the browser.
    - Create and track browser sessions.
    - Hide browser implementation details from the rest of AgentForge.

Must NOT do:
    - Perform page interactions.
    - Know about Playwright internals.
    - Contain application business logic.
"""

from __future__ import annotations

from app.browser_engine.exceptions.browser_errors import (
    BrowserLaunchError,
)
from app.browser_engine.factory.browser_factory import BrowserFactory
from app.browser_engine.interfaces.browser import Browser
from app.browser_engine.managers.session_manager import SessionManager
from app.browser_engine.models.browser_options import BrowserOptions


class BrowserManager:
    """
    High-level runtime manager for the Browser Engine.

    This class owns exactly one browser instance and manages the
    lifecycle of all browser sessions created from it.
    """

    def __init__(
        self,
        options: BrowserOptions | None = None,
    ) -> None:
        """
        Initialize the browser manager.

        Args:
            options:
                Browser launch configuration.
        """
        self._options = options or BrowserOptions()

        self._browser: Browser | None = None

        self._sessions: list[SessionManager] = []

    async def start(self) -> None:
        """
        Launch the browser.

        Calling this method multiple times has no effect.
        """
        if self.is_running:
            return

        self._browser = BrowserFactory.create_browser()

        await self._browser.launch(self._options)

    async def stop(self) -> None:
        """
        Close all sessions and stop the browser.
        """
        if not self.is_running:
            return

        await self.close_all_sessions()

        if self._browser is not None:
            await self._browser.close()

        self._browser = None

    async def create_session(self) -> SessionManager:
        """
        Create a managed browser session.

        Returns:
            SessionManager
        """
        if self._browser is None:
            raise BrowserLaunchError(
                "Browser has not been started."
            )

        session = await self._browser.new_session()

        manager = SessionManager(session)

        self._sessions.append(manager)

        return manager

    async def close_all_sessions(self) -> None:
        """
        Close every active browser session.
        """
        for session in list(self._sessions):
            await session.close()

        self._sessions.clear()

    @property
    def browser(self) -> Browser:
        """
        Return the managed browser.

        Raises:
            BrowserLaunchError
                If the browser has not been started.
        """
        if self._browser is None:
            raise BrowserLaunchError(
                "Browser has not been started."
            )

        return self._browser

    @property
    def session_count(self) -> int:
        """
        Return the number of active sessions.
        """
        return len(self._sessions)

    @property
    def is_running(self) -> bool:
        """
        Indicates whether the browser is currently running.
        """
        return (
            self._browser is not None
            and self._browser.is_running
        )