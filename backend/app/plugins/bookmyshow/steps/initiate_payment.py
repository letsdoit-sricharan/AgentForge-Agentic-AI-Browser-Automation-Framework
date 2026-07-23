"""
Purpose:
    Workflow step that initiates payment on BookMyShow.

Responsibilities:
    - Click the Pay button to proceed to the payment page.

Does NOT:
    - Process payment (that is the payment gateway's responsibility).
    - Import Playwright.
    - Contain page selectors.
"""

from __future__ import annotations

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.bookmyshow.pages.seat_page import SeatPage
from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class InitiatePaymentStep(BaseBookMyShowStep):
    """
    Workflow step: initiate the payment process by clicking Pay.
    """

    @property
    def name(self) -> str:
        return "initiate_payment"

    @property
    def success_message(self) -> str:
        return "Payment initiated successfully."

    async def perform(
        self,
        context: WorkflowContext,
    ) -> None:
        page = SeatPage(context)
        await page.proceed_to_pay()