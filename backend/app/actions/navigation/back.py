"""
Back navigation action.

Provides a reusable action for navigating
to the previous page.
"""

from __future__ import annotations

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.page import Page


class BackAction(BaseAction):
    """
    Navigate to the previous page.
    """

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Navigate back in browser history.
        """

        try:
            await page.go_back()

        except Exception as exc:
            raise ActionExecutionError(
                "Failed to navigate back."
            ) from exc