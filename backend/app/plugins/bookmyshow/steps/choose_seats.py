"""
Purpose:
    Workflow step that selects seats on BookMyShow.

Responsibilities:
    - Navigate to the seat selection interface.
    - Select the required number of seats.

Does NOT:
    - Import Playwright.
    - Contain page selectors (pending real-selector implementation).
"""

from __future__ import annotations

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class ChooseSeatsStep(BaseBookMyShowStep):
    """
    Workflow step: select seats in the theatre.

    TODO: Implement with real BookMyShow selectors in the plugin completion phase.
    """

    @property
    def name(self) -> str:
        return "choose_seats"

    @property
    def success_message(self) -> str:
        return "Seats selected successfully."

    async def perform(
        self,
        context: WorkflowContext,
    ) -> None:
        raise NotImplementedError(
            "ChooseSeatsStep.perform() requires real BookMyShow selectors. "
            "Implement in the plugin completion phase."
        )