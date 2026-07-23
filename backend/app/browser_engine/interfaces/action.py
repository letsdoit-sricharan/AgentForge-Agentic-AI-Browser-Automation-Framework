"""
Purpose:
    Defines the abstract Action interface for reusable browser actions.

Responsibilities:
    - Define a common execution contract.
    - Enable interchangeable browser actions.
    - Support future logging, tracing, and middleware.

Must NOT do:
    - Import Playwright.
    - Contain browser implementation logic.
    - Handle retries or business decisions.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Action(ABC):
    """
    Abstract interface representing a browser action.

    Concrete implementations encapsulate a single browser operation,
    such as clicking an element, filling a form field, or taking a
    screenshot.
    """

    @abstractmethod
    async def execute(self) -> None:
        """
        Execute the browser action.
        """
        raise NotImplementedError
