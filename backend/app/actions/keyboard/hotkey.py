"""
Hotkey action.

Provides a reusable action for executing
keyboard shortcuts consisting of multiple keys.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.page import Page


@dataclass
class HotkeyAction(BaseAction):
    """
    Reusable keyboard hotkey action.
    """

    keys: tuple[str, ...]

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Execute a keyboard hotkey.
        """

        try:
            await page.hotkey(*self.keys)

        except Exception as exc:
            raise ActionExecutionError(
                f"Failed to execute hotkey: {' + '.join(self.keys)}."
            ) from exc
