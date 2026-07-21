"""
Scroll To action.

Provides a reusable action for scrolling
to an absolute position on the page.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.page import Page


@dataclass
class ScrollToAction(BaseAction):
    """
    Reusable absolute page scroll action.
    """

    x: float
    y: float

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Scroll to the specified page coordinates.
        """

        try:
            await page.scroll_to(
                x=self.x,
                y=self.y,
            )

        except Exception as exc:
            raise ActionExecutionError(
                f"Failed to scroll to "
                f"({self.x}, {self.y})."
            ) from exc