"""
Focus action.

Provides a reusable action for focusing
a browser element.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.locator import Locator
from app.browser_engine.interfaces.page import Page


@dataclass()
class FocusAction(BaseAction):
    """
    Reusable focus action.
    """

    locator: Locator

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Focus the target element.
        """

        try:
            await self.locator.focus()

        except Exception as exc:
            raise ActionExecutionError(
                "Failed to focus the target element."
            ) from exc
