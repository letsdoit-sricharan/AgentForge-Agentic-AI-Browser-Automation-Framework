"""
Base class for all browser actions.

Every reusable browser action in AgentForge inherits
from BaseAction.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.browser_engine.interfaces.page import Page


class BaseAction(ABC):
    """
    Abstract base class for all browser actions.
    """

    @property
    def name(self) -> str:
        """
        Human-readable action name.
        """
        return self.__class__.__name__

    @abstractmethod
    async def execute(
        self,
        page: Page,
    ):
        """
        Execute the action.

        Args:
            page:
                Browser Engine page interface.

        Returns:
            Action-specific result.
        """
        raise NotImplementedError
