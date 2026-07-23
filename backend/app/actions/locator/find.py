"""
Find action.

Provides a reusable action for locating
an element on a page.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.locator import Locator
from app.browser_engine.interfaces.page import Page


@dataclass
class FindAction(BaseAction):
    """
    Reusable element lookup action.
    """

    selector: str

    async def execute(
        self,
        page: Page,
    ) -> Locator:
        """
        Locate and return a browser-agnostic Locator.
        """

        try:
            return page.locator(self.selector)

        except Exception as exc:
            raise ActionExecutionError(
                f"Failed to locate element '{self.selector}'."
            ) from exc
