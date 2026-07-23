"""
Uncheck action.

Provides a reusable action for unchecking
a checkbox.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.locator import Locator
from app.browser_engine.interfaces.page import Page


@dataclass()
class UncheckAction(BaseAction):
    """
    Reusable uncheck action.
    """

    locator: Locator

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Uncheck the target element.
        """

        try:
            await self.locator.uncheck()

        except Exception as exc:
            raise ActionExecutionError(
                "Failed to uncheck the target element."
            ) from exc
