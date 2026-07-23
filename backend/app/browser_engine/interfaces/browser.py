"""
Purpose:
    Defines the abstract Browser interface for the AgentForge Browser Engine.

Responsibilities:
    - Define the lifecycle contract for a browser instance.
    - Define how browser sessions are created.
    - Expose the browser's runtime state.

Must NOT do:
    - Import or expose Playwright.
    - Contain implementation logic.
    - Manage browser pages directly.
    - Handle logging, configuration, or retries.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.browser_engine.interfaces.session import Session


class Browser(ABC):
    """
    Abstract interface representing a browser instance.

    This interface defines the contract that every browser backend
    (e.g., Playwright, Selenium, Browserbase) must implement.

    High-level modules such as BrowserManager should depend only on
    this interface and never on a specific browser implementation.
    """

    @abstractmethod
    async def launch(self) -> None:
        """
        Launch the browser.

        Raises:
            BrowserLaunchError:
                Raised if the browser cannot be started.
        """
        raise NotImplementedError

    @abstractmethod
    async def new_session(self) -> Session:
        """
        Create a new isolated browser session.

        Returns:
            Session:
                A browser session that manages pages, cookies,
                storage, and other session-specific resources.
        """
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        """
        Close the browser and release all associated resources.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def is_running(self) -> bool:
        """
        Indicates whether the browser is currently running.

        Returns:
            bool:
                True if the browser is running, otherwise False.
        """
        raise NotImplementedError
