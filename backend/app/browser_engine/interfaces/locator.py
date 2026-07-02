"""
Purpose:
    Define the interface for the Locator component of the AgentForge Browser Engine.
    This interface abstracts an element locator (e.g., Playwright's Locator)
    and provides a standard set of methods for interacting with elements on a page.

Responsibilities:
    - Define abstract methods to interact with matched elements (click, fill, hover, check).
    - Define abstract methods to inspect element state (is_visible, is_enabled, text_content).
    - Define abstract methods to wait for element states.
    - Support querying multiple matched elements (count, nth locator).

Must NOT do:
    - Import or reference Playwright-specific objects or exceptions.
    - Implement concrete selector parsing or evaluation logic.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional, List


class Locator(ABC):
    """
    Abstract base class representing an element locator.
    """

    @abstractmethod
    async def click(self, options: Optional[Any] = None) -> None:
        """
        Click the element(s) matched by this locator.

        Args:
            options: Configuration options for the click (e.g. timeout, force, modifiers).
        """
        pass

    @abstractmethod
    async def fill(self, value: str, options: Optional[Any] = None) -> None:
        """
        Fill the input element matched by this locator with the specified value.

        Args:
            value: The string value to enter.
            options: Configuration options for filling.
        """
        pass

    @abstractmethod
    async def hover(self, options: Optional[Any] = None) -> None:
        """
        Hover the pointer over the element matched by this locator.

        Args:
            options: Configuration options for hovering.
        """
        pass

    @abstractmethod
    async def check(self, options: Optional[Any] = None) -> None:
        """
        Check the checkbox or radio button matched by this locator.

        Args:
            options: Configuration options for checking.
        """
        pass

    @abstractmethod
    async def uncheck(self, options: Optional[Any] = None) -> None:
        """
        Uncheck the checkbox matched by this locator.

        Args:
            options: Configuration options for unchecking.
        """
        pass

    @abstractmethod
    async def text_content(self) -> Optional[str]:
        """
        Retrieve the text content of the element matched by this locator.

        Returns:
            The text content as a string, or None if the element has no text content.
        """
        pass

    @abstractmethod
    async def inner_text(self) -> str:
        """
        Retrieve the inner text of the element matched by this locator.

        Returns:
            The inner text as a string.
        """
        pass

    @abstractmethod
    async def get_attribute(self, name: str) -> Optional[str]:
        """
        Retrieve the value of an attribute of the element matched by this locator.

        Args:
            name: The name of the attribute.

        Returns:
            The attribute value as a string, or None if the attribute is missing.
        """
        pass

    @abstractmethod
    async def is_visible(self) -> bool:
        """
        Check if the element matched by this locator is visible on the page.

        Returns:
            True if visible, False otherwise.
        """
        pass

    @abstractmethod
    async def is_enabled(self) -> bool:
        """
        Check if the element matched by this locator is enabled.

        Returns:
            True if enabled, False otherwise.
        """
        pass

    @abstractmethod
    async def wait_for(self, state: Optional[str] = None, timeout: Optional[float] = None) -> None:
        """
        Wait for the element matched by this locator to reach a specific state.

        Args:
            state: The target element state (e.g. 'visible', 'hidden', 'attached', 'detached').
            timeout: Optional maximum wait time in milliseconds.
        """
        pass

    @abstractmethod
    async def count(self) -> int:
        """
        Return the number of elements matched by this locator.

        Returns:
            The count of matched elements.
        """
        pass

    @abstractmethod
    def nth(self, index: int) -> Locator:
        """
        Create a new locator that points to the nth matched element.

        Args:
            index: The 0-based index of the element.

        Returns:
            A new Locator instance.
        """
        pass
