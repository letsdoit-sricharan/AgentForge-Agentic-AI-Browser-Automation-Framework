"""
Drag and Drop action.

Provides a reusable action for dragging an
element from one location to another.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.page import Page


@dataclass
class DragAndDropAction(BaseAction):
    """
    Reusable drag-and-drop action.
    """

    source_selector: str
    target_selector: str

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Drag an element from the source selector
        to the target selector.
        """

        try:
            await page.drag_and_drop(
                self.source_selector,
                self.target_selector,
            )

        except Exception as exc:
            raise ActionExecutionError(
                f"Failed to drag '{self.source_selector}' "
                f"to '{self.target_selector}'."
            ) from exc
