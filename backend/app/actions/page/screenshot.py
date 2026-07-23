"""
Screenshot action.

Provides a reusable action for capturing
a screenshot of the current page.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.page import Page
from app.browser_engine.models.screenshot_options import ScreenshotOptions


@dataclass
class ScreenshotAction(BaseAction):
    """
    Reusable screenshot action.
    """

    options: ScreenshotOptions

    async def execute(
        self,
        page: Page,
    ) -> Path:
        """
        Capture a screenshot of the current page.

        Returns:
            Path:
                Filesystem path of the saved screenshot.
        """

        try:
            return await page.screenshot(self.options)

        except Exception as exc:
            raise ActionExecutionError(
                "Failed to capture screenshot."
            ) from exc
