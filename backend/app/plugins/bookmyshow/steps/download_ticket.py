"""
Purpose:
    Workflow step that downloads the booking ticket on BookMyShow.

Responsibilities:
    - Locate the ticket download interface after payment.
    - Trigger the download.
    - Return the downloaded file path.

Does NOT:
    - Process payment.
    - Import Playwright.
    - Contain page selectors (pending real-selector implementation).
"""

from __future__ import annotations

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class DownloadTicketStep(BaseBookMyShowStep):
    """
    Workflow step: download the booking confirmation ticket.

    TODO: Implement with real BookMyShow selectors in the plugin completion phase.
    """

    @property
    def name(self) -> str:
        return "download_ticket"

    @property
    def success_message(self) -> str:
        return "Ticket downloaded successfully."

    async def perform(
        self,
        context: WorkflowContext,
    ) -> None:
        raise NotImplementedError(
            "DownloadTicketStep.perform() requires real BookMyShow selectors. "
            "Implement in the plugin completion phase."
        )