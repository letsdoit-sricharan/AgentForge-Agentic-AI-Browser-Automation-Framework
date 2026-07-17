"""
Navigation action.

Provides a reusable action for navigating to a URL.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.page import Page
from app.browser_engine.models.navigation_options import NavigationOptions


@dataclass()
class NavigateAction(BaseAction):
    """
    Reusable browser navigation action.
    """

    url: str

    options: NavigationOptions | None = None

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Navigate the page to the configured URL.
        """

        try:
            await page.goto(
                self.url,
                self.options,
            )

        except Exception as exc:
            raise ActionExecutionError(
                f"Failed to navigate to '{self.url}'."
            ) from exc