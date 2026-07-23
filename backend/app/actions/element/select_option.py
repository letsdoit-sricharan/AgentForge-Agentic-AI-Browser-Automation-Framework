"""
Select option action.

Provides a reusable action for selecting
an option from a dropdown element.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.locator import Locator
from app.browser_engine.interfaces.page import Page


@dataclass()
class SelectOptionAction(BaseAction):
    """
    Reusable dropdown selection action.
    """

    locator: Locator
    value: str

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Select an option by value.
        """

        try:
            await self.locator.select_option(self.value)

        except Exception as exc:
            raise ActionExecutionError(
                f"Failed to select option '{self.value}'."
            ) from exc
