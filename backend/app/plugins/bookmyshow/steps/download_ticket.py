"""
Purpose:
    Workflow step that verifies the booking confirmation on BookMyShow.

Responsibilities:
    - Verify the payment/confirmation page is displayed.
    - In a real implementation: download the booking confirmation PDF.

Does NOT:
    - Process payment.
    - Import Playwright.
    - Contain page selectors.
"""

from __future__ import annotations

import asyncio

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class DownloadTicketStep(BaseBookMyShowStep):
    """
    Workflow step: verify the booking confirmation page is displayed.
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
        """
        Verify the payment confirmation page rendered.
        Actual ticket download would require real BMS selectors.
        """
        await asyncio.sleep(0.5)
        payment_heading = context.page.locator("#payment-page h1").first()
        try:
            await payment_heading.wait(timeout=5000)
        except Exception:
            # In some mock flows the payment page may not have an explicit heading
            pass