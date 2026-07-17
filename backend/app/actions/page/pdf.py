"""
PDF action.

Provides a reusable action for saving
the current page as a PDF.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.page import Page


@dataclass(slots=True)
class PdfAction(BaseAction):
    """
    Reusable PDF generation action.
    """

    path: Path

    async def execute(
        self,
        page: Page,
    ) -> Path:
        """
        Save the current page as a PDF.

        Returns:
            Path to the generated PDF.
        """

        try:
            return await page.pdf(self.path)

        except Exception as exc:
            raise ActionExecutionError(
                f"Failed to generate PDF at '{self.path}'."
            ) from exc