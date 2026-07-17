"""
Check action.

Provides a reusable action for checking
a checkbox or radio button.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.locator import Locator
from app.browser_engine.interfaces.page import Page


@dataclass()
class CheckAction(BaseAction):
    """
    Reusable check action.
    """

    locator: Locator

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Check the target element.
        """

        try:
            await self.locator.check()

        except Exception as exc:
            raise ActionExecutionError(
                "Failed to check the target element."
            ) from exc