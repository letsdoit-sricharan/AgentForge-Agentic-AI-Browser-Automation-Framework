"""
Purpose:
    High-level manager responsible for controlling the browser runtime.

Responsibilities:
    - Own a single browser instance.
    - Launch and stop the browser.
    - Create and track browser sessions.
    - Automatically unregister closed sessions.

Must NOT:
    - Perform page interactions.
    - Know about Playwright.
    - Contain business logic.
"""

from __future__ import annotations

from app.browser_engine.exceptions.browser_errors import (
    BrowserClosedError,
    BrowserLaunchError,
)
from app.browser_engine.factory.browser_factory import BrowserFactory
from app.browser_engine.interfaces.browser import Browser
from app.browser_engine.managers.session_manager import SessionManager
from app.browser_engine.models.browser_options import BrowserOptions


class BrowserManager:
    """
    High-level runtime manager for the Browser Engine.
    """

    def __init__(
        self,
        options: BrowserOptions | None = None,
    ) -> None:

        self._options = options or BrowserOptions()

        self._browser: Browser | None = None

        self._sessions: dict[str, SessionManager] = {}

        self._sessions: dict[str, SessionManager] = {}

        self._started = False

    async def start(self) -> None:
        """
        Launch the browser.
        """
        if self.is_running:
            return

        self._browser = BrowserFactory.create_browser()

        await self._browser.launch(self._options)

        self._started = True

    async def stop(self) -> None:
        """
        Stop the browser and close all active sessions.
        """
        if not self.is_running:
            return

        await self.close_all_sessions()

        await self._browser.close()

        self._browser = None

    async def create_session(self) -> SessionManager:
        """
        Create and register a new browser session.
        """
        if self._browser is None:

            if self._started:
                raise BrowserClosedError(
                    "Browser has already been stopped."
                )

            raise BrowserLaunchError(
                "Browser has not been started."
            )

        session = await self._browser.new_session()

        manager = SessionManager(
            session=session,
            on_close=self._remove_session,
        )

        self._sessions[manager.id] = manager

        return manager

    async def close_all_sessions(self) -> None:
        """
        Close every active session.
        """
        sessions = list(self._sessions.values())

        for session in sessions:
            await session.close()

    def _remove_session(
        self,
        session_id: str,
    ) -> None:
        """
        Remove a closed session.
        """
        self._sessions.pop(session_id, None)

    def get_session(
        self,
        session_id: str,
    ) -> SessionManager | None:
        """
        Retrieve a session by its ID.
        """
        return self._sessions.get(session_id)

    @property
    def browser(self) -> Browser:
        """
        Return the managed browser.
        """
        if self._browser is None:

            if self._started:
                raise BrowserClosedError(
                    "Browser has already been stopped."
                )

            raise BrowserLaunchError(
                "Browser has not been started."
            )

        return self._browser

    @property
    def session_count(self) -> int:
        """
        Number of active sessions.
        """
        return len(self._sessions)

    @property
    def sessions(self) -> tuple[SessionManager, ...]:
        """
        Immutable view of active sessions.
        """
        return tuple(self._sessions.values())

    @property
    def is_running(self) -> bool:
        """
        Whether the browser is running.
        """
        return (
            self._browser is not None
            and self._browser.is_running
        )