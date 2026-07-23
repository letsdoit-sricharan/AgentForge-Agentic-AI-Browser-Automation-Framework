"""
Evaluate action.

Provides a reusable action for executing
JavaScript in the current page.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.page import Page


@dataclass
class EvaluateAction(BaseAction):
    """
    Reusable JavaScript evaluation action.
    """

    script: str
    argument: object | None = None

    async def execute(
        self,
        page: Page,
    ) -> object:
        """
        Execute JavaScript in the page.

        Returns:
            The value returned by the JavaScript execution.
        """

        try:
            return await page.evaluate(
                script=self.script,
                argument=self.argument,
            )

        except Exception as exc:
            raise ActionExecutionError(
                "Failed to evaluate JavaScript."
            ) from exc
