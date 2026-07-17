"""
Download action.

Provides a reusable action for waiting
for a browser download to complete.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.page import Page


@dataclass(slots=True)
class DownloadAction(BaseAction):
    """
    Reusable file download action.
    """

    async def execute(
        self,
        page: Page,
    ) -> Path:
        """
        Wait for the next download.

        Returns:
            Path:
                Location of the downloaded file.
        """

        try:
            return await page.expect_download()

        except Exception as exc:
            raise ActionExecutionError(
                "Failed to download file."
            ) from exc