"""
Purpose:
    Playwright implementation of the Browser interface.

Responsibilities:
    - Launch and close the browser.
    - Create browser sessions.
    - Hide Playwright browser objects from the rest of AgentForge.

Must NOT do:
    - Manage the Playwright runtime.
    - Perform page actions.
    - Perform business logic.
"""

from __future__ import annotations

from playwright.async_api import Browser as PlaywrightBrowserInstance

from app.browser_engine.implementations.playwright.playwright_adapter import (
    PlaywrightAdapter,
)
from app.browser_engine.implementations.playwright.playwright_session import (
    PlaywrightSession,
)
from app.browser_engine.interfaces.browser import Browser
from app.browser_engine.interfaces.session import Session
from app.browser_engine.models.browser_options import BrowserOptions


class PlaywrightBrowser(Browser):
    """
    Playwright implementation of the Browser interface.
    """

    def __init__(
        self,
        adapter: PlaywrightAdapter,
    ) -> None:
        """
        Initialize the browser implementation.

        Args:
            adapter:
                Playwright runtime adapter.
        """
        self._adapter = adapter
        self._browser: PlaywrightBrowserInstance | None = None
        self._options: BrowserOptions | None = None

    async def launch(
        self,
        options: BrowserOptions,
    ) -> None:
        """
        Launch the browser.

        Args:
            options:
                Browser launch configuration.
        """
        await self._adapter.start()
        self._browser = await self._adapter.launch_browser(options)
        self._options = options

    async def close(self) -> None:
        """
        Close the browser and stop the Playwright runtime.
        """
        if self._browser is not None:
            await self._browser.close()
            self._browser = None

        await self._adapter.stop()

    async def new_session(self) -> Session:
        """
        Create a new browser session.

        Returns:
            Session implementation.
        """
        if self._browser is None:
            raise RuntimeError(
                "Browser has not been launched."
            )

        context_kwargs: dict = {}

        if self._options is not None:
            if self._options.user_agent is not None:
                context_kwargs["user_agent"] = self._options.user_agent

            vp = self._options.viewport
            context_kwargs["viewport"] = {
                "width": vp.width,
                "height": vp.height,
            }

        context = await self._browser.new_context(**context_kwargs)

        return PlaywrightSession(context)

    @property
    def is_running(self) -> bool:
        """
        Indicates whether the browser has been launched.
        """
        return self._browser is not None