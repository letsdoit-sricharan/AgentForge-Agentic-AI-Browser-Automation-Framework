"""
Wait for element action.

Provides a reusable action for waiting until
an element becomes available.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.locator import Locator
from app.browser_engine.interfaces.page import Page


@dataclass
class WaitForElementAction(BaseAction):
    """
    Wait until an element becomes available.
    """

    selector: str
    timeout: int | None = None

    async def execute(
        self,
        page: Page,
    ) -> Locator:
        """
        Locate the element and wait until it is available.
        """

        try:
            locator = page.locator(self.selector)
            await locator.wait(self.timeout)
            return locator

        except Exception as exc:
            raise ActionExecutionError(
                f"Timed out waiting for '{self.selector}'."
            ) from exc