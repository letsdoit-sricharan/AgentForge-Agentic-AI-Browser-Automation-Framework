"""
Press Key action.

Provides a reusable action for pressing
a keyboard key.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.page import Page


@dataclass
class PressKeyAction(BaseAction):
    """
    Reusable keyboard press action.
    """

    key: str

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Press a keyboard key.
        """

        try:
            await page.press_key(self.key)

        except Exception as exc:
            raise ActionExecutionError(
                f"Failed to press key '{self.key}'."
            ) from exc