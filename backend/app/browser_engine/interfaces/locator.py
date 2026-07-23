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
    async def click(self, force: bool = False) -> None:
        """
        Click the element.

        Args:
            force: Whether to bypass actionability checks.
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

    @abstractmethod
    def first(self) -> "Locator":
        """
        Return a locator representing the first matching element.
        """
        raise NotImplementedError

    @abstractmethod
    def last(self) -> "Locator":
        """
        Return a locator representing the last matching element.
        """
        raise NotImplementedError

    @abstractmethod
    def nth(self, index: int) -> "Locator":
        """
        Return a locator representing the nth matching element.

        Args:
            index:
                Zero-based index of the element.
        """
        raise NotImplementedError

    @abstractmethod
    async def wait_until_hidden(
        self,
        timeout: int | None = None,
    ) -> None:
        """
        Wait until the element becomes hidden.

        Args:
            timeout:
                Optional timeout in milliseconds.
        """
        raise NotImplementedError

    @abstractmethod
    async def scroll_into_view(self) -> None:
        """
        Scroll the element into the visible viewport.
        """
        raise NotImplementedError

    @abstractmethod
    def filter(self, has_text: str | None = None) -> "Locator":
        """
        Return a locator narrowed by filter criteria.

        Args:
            has_text: Optional text that the element must contain.
        """
        raise NotImplementedError

    @abstractmethod
    def locator(self, selector: str) -> "Locator":
        """
        Find an element matching the selector inside this locator.

        Args:
            selector: CSS or text selector.
        """
        raise NotImplementedError

    @abstractmethod
    async def bounding_box(self) -> dict | None:
        """
        Get the bounding box of the element.
        Returns a dictionary with x, y, width, height, or None if not visible.
        """
        raise NotImplementedError
