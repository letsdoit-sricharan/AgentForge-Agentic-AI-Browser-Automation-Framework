"""
Upload action.

Provides a reusable action for uploading
a file through a file input element.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.page import Page


@dataclass
class UploadAction(BaseAction):
    """
    Reusable file upload action.
    """

    selector: str
    file_path: Path

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Upload a file.
        """

        try:
            await page.upload_file(
                selector=self.selector,
                file_path=self.file_path,
            )

        except Exception as exc:
            raise ActionExecutionError(
                f"Failed to upload file '{self.file_path}'."
            ) from exc