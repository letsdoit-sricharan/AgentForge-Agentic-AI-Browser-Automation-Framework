"""
Type Text action.

Provides a reusable action for typing
text using the keyboard.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.page import Page


@dataclass
class TypeTextAction(BaseAction):
    """
    Reusable keyboard typing action.
    """

    text: str
    delay: float | None = None

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Type text using keyboard input.
        """

        try:
            await page.type_text(
                self.text,
                self.delay,
            )

        except Exception as exc:
            raise ActionExecutionError(
                "Failed to type text."
            ) from exc
