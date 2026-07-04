"""
Purpose:
    Defines the abstract Locator interface for the AgentForge Browser Engine.

Responsibilities:
    - Define element-level interactions.
    - Hide browser automation implementation details.
    - Provide a consistent API for interacting with page elements.

Must NOT do:
    - Import Playwright.
    - Contain implementation logic.
    - Manage browser, sessions, or pages.
    - Handle logging or retries.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Locator(ABC):
    """
    Abstract interface representing a page element.

    Concrete implementations must provide browser-specific behavior
    while exposing a consistent API to the rest of AgentForge.
    """

    @abstractmethod
    async def click(self) -> None:
        """
        Click the element.
        """
        raise NotImplementedError

    @abstractmethod
    async def fill(self, value: str) -> None:
        """
        Fill the element with the given value.
        """
        raise NotImplementedError

    @abstractmethod
    async def text(self) -> str:
        """
        Return the visible text of the element.
        """
        raise NotImplementedError

    @abstractmethod
    async def is_visible(self) -> bool:
        """
        Check whether the element is visible.

        Returns:
            bool: True if the element is visible.
        """
        raise NotImplementedError

    @abstractmethod
    async def hover(self) -> None:
        """
        Hover over the element.
        """
        raise NotImplementedError

    @abstractmethod
    async def select(self, value: str) -> None:
        """
        Select an option from a dropdown.
        """
        raise NotImplementedError

    @abstractmethod
    async def wait(self, timeout: int | None = None) -> None:
        """
        Wait until the element becomes available.

        Args:
            timeout: Optional timeout in milliseconds.
        """
        raise NotImplementedError