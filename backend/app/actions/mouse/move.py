"""
Move Mouse action.

Provides a reusable action for moving
the mouse cursor.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.page import Page


@dataclass
class MoveMouseAction(BaseAction):
    """
    Reusable mouse movement action.
    """

    x: float
    y: float

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Move the mouse cursor.
        """

        try:
            await page.move_mouse(
                self.x,
                self.y,
            )

        except Exception as exc:
            raise ActionExecutionError(
                f"Failed to move mouse to ({self.x}, {self.y})."
            ) from exc
