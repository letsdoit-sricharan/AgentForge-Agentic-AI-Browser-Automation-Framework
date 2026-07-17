"""
Hover action.

Provides a reusable action for hovering
over a browser element.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.locator import Locator
from app.browser_engine.interfaces.page import Page


@dataclass()
class HoverAction(BaseAction):
    """
    Reusable hover action.
    """

    locator: Locator

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Execute the hover action.
        """

        try:
            await self.locator.hover()

        except Exception as exc:
            raise ActionExecutionError(
                "Failed to hover over the target element."
            ) from exc