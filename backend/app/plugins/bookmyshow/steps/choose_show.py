"""
Purpose:
    Workflow step that selects a specific show/screening on BookMyShow.

Responsibilities:
    - Navigate to the show listing.
    - Select the target show time.

Does NOT:
    - Import Playwright.
    - Contain page selectors (pending real-selector implementation).
"""

from __future__ import annotations

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class ChooseShowStep(BaseBookMyShowStep):
    """
    Workflow step: select the specific show/screening time.

    TODO: Implement with real BookMyShow selectors in the plugin completion phase.
    """

    @property
    def name(self) -> str:
        return "choose_show"

    @property
    def success_message(self) -> str:
        return "Show selected successfully."

    async def perform(
        self,
        context: WorkflowContext,
    ) -> None:
        raise NotImplementedError(
            "ChooseShowStep.perform() requires real BookMyShow selectors. "
            "Implement in the plugin completion phase."
        )