"""
Drag action.

Provides a reusable action for dragging
the mouse from one coordinate to another.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.page import Page


@dataclass
class DragAction(BaseAction):
    """
    Reusable mouse drag action.
    """

    start_x: float
    start_y: float
    end_x: float
    end_y: float

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Drag the mouse from the start position
        to the end position.
        """

        try:
            await page.drag(
                start_x=self.start_x,
                start_y=self.start_y,
                end_x=self.end_x,
                end_y=self.end_y,
            )

        except Exception as exc:
            raise ActionExecutionError(
                f"Failed to drag mouse from "
                f"({self.start_x}, {self.start_y}) "
                f"to ({self.end_x}, {self.end_y})."
            ) from exc
