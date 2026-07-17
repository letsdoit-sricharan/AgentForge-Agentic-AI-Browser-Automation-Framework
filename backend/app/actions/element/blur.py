"""
Blur action.

Provides a reusable action for removing
focus from a browser element.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.locator import Locator
from app.browser_engine.interfaces.page import Page


@dataclass()
class BlurAction(BaseAction):
    """
    Reusable blur action.
    """

    locator: Locator

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Remove focus from the target element.
        """

        try:
            await self.locator.blur()

        except Exception as exc:
            raise ActionExecutionError(
                "Failed to blur the target element."
            ) from exc