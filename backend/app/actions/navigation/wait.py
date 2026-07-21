"""
Wait action.

Provides a reusable action for waiting until the page
reaches a desired load state.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.actions.base_action import BaseAction
from app.actions.exceptions import ActionExecutionError
from app.browser_engine.interfaces.page import Page
from app.browser_engine.models.load_state import LoadState


@dataclass
class WaitAction(BaseAction):
    """
    Wait for the page to reach a specific load state.
    """

    load_state: LoadState = LoadState.LOAD

    timeout: int | None = None

    async def execute(
        self,
        page: Page,
    ) -> None:
        """
        Wait until the page reaches the configured load state.
        """

        try:
            await page.wait_for_load(
                state=self.load_state,
                timeout=self.timeout,
            )

        except Exception as exc:
            raise ActionExecutionError(
                f"Failed while waiting for load state '{self.load_state.name}'."
            ) from exc