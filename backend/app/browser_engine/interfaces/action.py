"""
Purpose:
    Define the interface for Action components in the AgentForge Browser Engine.
    This supports command-pattern actions that can be executed dynamically on page objects.

Responsibilities:
    - Define an abstract method `execute` that runs a specific page action or sequence.
    - Standardize parameters and returns for action execution.

Must NOT do:
    - Implement concrete click, fill, or scroll actions.
    - Expose library-specific classes.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from app.browser_engine.interfaces.page import Page


class Action(ABC):
    """
    Abstract base class representing a reusable browser action or sequence.
    """

    @abstractmethod
    async def execute(self, page: Page) -> Any:
        """
        Execute the custom browser action on the provided page.

        Args:
            page: The Page instance to perform the action on.

        Returns:
            The output of the action execution, if any.
        """
        pass
