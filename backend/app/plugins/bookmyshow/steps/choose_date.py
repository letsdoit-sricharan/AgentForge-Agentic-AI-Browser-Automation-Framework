"""
Purpose:
    Workflow step that selects a show date on BookMyShow.

Responsibilities:
    - Navigate to the date selection interface.
    - Select the requested show date.

Does NOT:
    - Import Playwright.
    - Contain page selectors (pending real-selector implementation).
"""

from __future__ import annotations

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class ChooseDateStep(BaseBookMyShowStep):
    """
    Workflow step: select the show date.

    TODO: Implement with real BookMyShow selectors in the plugin completion phase.
    """

    @property
    def name(self) -> str:
        return "choose_date"

    @property
    def success_message(self) -> str:
        return "Show date selected successfully."

    async def perform(
        self,
        context: WorkflowContext,
    ) -> None:
        raise NotImplementedError(
            "ChooseDateStep.perform() requires real BookMyShow selectors. "
            "Implement in the plugin completion phase."
        )