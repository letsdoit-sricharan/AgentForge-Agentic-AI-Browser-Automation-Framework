"""
Wait Until Hidden action.

Provides a reusable action for waiting until
an element becomes hidden.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.page import Page


@dataclass
class WaitUntilHiddenAction(BaseAction):
    """
    Wait until an element becomes hidden.
    """

    selector: str
    timeout: int | None = None

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Wait until the specified element becomes hidden.
        """

        try:
            locator = page.locator(self.selector)
            await locator.wait_until_hidden(self.timeout)

        except Exception as exc:
            raise ActionExecutionError(
                f"Timed out waiting for '{self.selector}' to become hidden."
            ) from exc