"""
Mouse Wheel action.

Provides a reusable action for scrolling
the mouse wheel.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.page import Page


@dataclass
class MouseWheelAction(BaseAction):
    """
    Reusable mouse wheel scrolling action.
    """

    delta_x: float = 0.0
    delta_y: float = 0.0

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Scroll the mouse wheel.
        """

        try:
            await page.mouse_wheel(
                self.delta_x,
                self.delta_y,
            )

        except Exception as exc:
            raise ActionExecutionError(
                f"Failed to scroll mouse wheel "
                f"(delta_x={self.delta_x}, "
                f"delta_y={self.delta_y})."
            ) from exc