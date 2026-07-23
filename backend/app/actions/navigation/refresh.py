"""
Refresh navigation action.

Provides a reusable action for refreshing
the current page.
"""

from __future__ import annotations

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.page import Page


class RefreshAction(BaseAction):
    """
    Refresh the current page.
    """

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Reload the current page.
        """

        try:
            await page.reload()

        except Exception as exc:
            raise ActionExecutionError(
                "Failed to refresh the page."
            ) from exc
