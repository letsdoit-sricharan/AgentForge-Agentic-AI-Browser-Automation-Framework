"""
Clear action.

Provides a reusable action for clearing
the contents of a browser element.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.locator import Locator
from app.browser_engine.interfaces.page import Page


@dataclass()
class ClearAction(BaseAction):
    """
    Reusable clear action.
    """

    locator: Locator

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Clear the target element.
        """

        try:
            await self.locator.clear()

        except Exception as exc:
            raise ActionExecutionError(
                "Failed to clear the target element."
            ) from exc