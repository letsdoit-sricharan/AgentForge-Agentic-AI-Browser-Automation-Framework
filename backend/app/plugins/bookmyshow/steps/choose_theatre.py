"""
Purpose:
    Workflow step that selects a theatre on BookMyShow.

Responsibilities:
    - Navigate to the theatre listing.
    - Select the preferred theatre.

Does NOT:
    - Import Playwright.
    - Contain page selectors (pending real-selector implementation).
"""

from __future__ import annotations

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class ChooseTheatreStep(BaseBookMyShowStep):
    """
    Workflow step: select the preferred theatre from the listing.

    TODO: Implement with real BookMyShow selectors in the plugin completion phase.
    """

    @property
    def name(self) -> str:
        return "choose_theatre"

    @property
    def success_message(self) -> str:
        return "Theatre selected successfully."

    async def perform(
        self,
        context: WorkflowContext,
    ) -> None:
        raise NotImplementedError(
            "ChooseTheatreStep.perform() requires real BookMyShow selectors. "
            "Implement in the plugin completion phase."
        )