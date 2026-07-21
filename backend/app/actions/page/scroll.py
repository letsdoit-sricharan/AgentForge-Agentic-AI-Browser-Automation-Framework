"""
Scroll action.

Provides a reusable action for scrolling
the current page.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.page import Page


@dataclass
class ScrollAction(BaseAction):
    """
    Reusable page scroll action.
    """

    delta_x: float = 0
    delta_y: float = 0

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Scroll the page.
        """

        try:
            await page.scroll(
                delta_x=self.delta_x,
                delta_y=self.delta_y,
            )

        except Exception as exc:
            raise ActionExecutionError(
                f"Failed to scroll page "
                f"(delta_x={self.delta_x}, "
                f"delta_y={self.delta_y})."
            ) from exc