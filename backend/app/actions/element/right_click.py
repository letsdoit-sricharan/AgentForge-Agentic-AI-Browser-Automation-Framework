"""
Right click action.

Provides a reusable action for right-clicking
a browser element.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.locator import Locator
from app.browser_engine.interfaces.page import Page


@dataclass()
class RightClickAction(BaseAction):
    """
    Reusable right-click action.
    """

    locator: Locator

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Execute the right-click action.
        """

        try:
            await self.locator.right_click()

        except Exception as exc:
            raise ActionExecutionError(
                "Failed to right-click the target element."
            ) from exc
