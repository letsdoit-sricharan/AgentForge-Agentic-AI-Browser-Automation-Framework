"""
Fill action.

Provides a reusable action for entering text
into a browser element.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.locator import Locator
from app.browser_engine.interfaces.page import Page


@dataclass()
class FillAction(BaseAction):
    """
    Reusable fill action.
    """

    locator: Locator
    text: str

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Fill the target element with text.
        """

        try:
            await self.locator.fill(self.text)

        except Exception as exc:
            raise ActionExecutionError(
                "Failed to fill the target element."
            ) from exc
