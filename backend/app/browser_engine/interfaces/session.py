"""
Purpose:
    Defines the abstract Session interface for the AgentForge Browser Engine.

Responsibilities:
    - Define the lifecycle of an isolated browser session.
    - Define how pages are created within a session.
    - Expose the session's runtime state.

Must NOT do:
    - Import or expose Playwright.
    - Contain implementation logic.
    - Manage browser lifecycle.
    - Perform page interactions.
    - Handle logging, retries, or configuration.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.browser_engine.interfaces.page import Page


class Session(ABC):
    """
    Abstract interface representing an isolated browser session.

    A session encapsulates browser state such as cookies,
    storage, authentication, and pages.

    Concrete implementations (e.g., PlaywrightSession)
    must implement this contract.
    """

    @abstractmethod
    async def new_page(self) -> Page:
        """
        Create a new page within this browser session.

        Returns:
            Page:
                A new browser page.
        """
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        """
        Close the browser session and release its resources.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def is_active(self) -> bool:
        """
        Indicates whether the session is currently active.

        Returns:
            bool:
                True if the session is active, otherwise False.
        """
        raise NotImplementedError
