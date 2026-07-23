"""
Shortcut action.

Provides a reusable action for executing
named keyboard shortcuts.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.page import Page

_SHORTCUTS: dict[str, tuple[str, ...]] = {
    "copy": ("Control", "C"),
    "paste": ("Control", "V"),
    "cut": ("Control", "X"),
    "undo": ("Control", "Z"),
    "redo": ("Control", "Y"),
    "select_all": ("Control", "A"),
    "save": ("Control", "S"),
}


@dataclass
class ShortcutAction(BaseAction):
    """
    Execute a named keyboard shortcut.
    """

    shortcut: str

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Execute the configured shortcut.
        """

        try:
            keys = _SHORTCUTS[self.shortcut.lower()]
        except KeyError as exc:
            raise ActionExecutionError(
                f"Unknown shortcut '{self.shortcut}'."
            ) from exc

        try:
            await page.hotkey(*keys)

        except Exception as exc:
            raise ActionExecutionError(
                f"Failed to execute shortcut '{self.shortcut}'."
            ) from exc
