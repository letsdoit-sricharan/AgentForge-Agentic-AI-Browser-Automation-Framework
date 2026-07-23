"""
Scroll Into View action.

Provides a reusable action for scrolling
an element into the visible viewport.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.locator import Locator
from app.browser_engine.interfaces.page import Page


@dataclass
class ScrollIntoViewAction(BaseAction):
    """
    Reusable action for scrolling an element
    into the visible viewport.
    """

    locator: Locator

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Scroll the element into view.

        The page parameter is accepted to maintain
        a consistent action interface.
        """

        try:
            await self.locator.scroll_into_view()

        except Exception as exc:
            raise ActionExecutionError(
                "Failed to scroll element into view."
            ) from exc
