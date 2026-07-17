"""
Click action.

Provides a reusable action for clicking
a browser element.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.locator import Locator
from app.browser_engine.interfaces.page import Page


@dataclass()
class ClickAction(BaseAction):
    """
    Reusable click action.
    """

    locator: Locator

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Execute the click action.

        The page parameter is accepted to maintain a
        consistent interface with all actions, although
        this action operates directly on the locator.
        """

        try:
            await self.locator.click()

        except Exception as exc:
            raise ActionExecutionError(
                "Failed to click the target element."
            ) from exc