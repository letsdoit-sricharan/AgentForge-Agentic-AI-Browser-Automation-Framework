"""
Forward navigation action.

Provides a reusable action for navigating
to the next page.
"""

from __future__ import annotations

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.page import Page


class ForwardAction(BaseAction):
    """
    Navigate to the next page.
    """

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Navigate forward in browser history.
        """

        try:
            await page.go_forward()

        except Exception as exc:
            raise ActionExecutionError(
                "Failed to navigate forward."
            ) from exc
