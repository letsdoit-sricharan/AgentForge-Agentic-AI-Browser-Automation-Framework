"""
Purpose:
    Workflow step that initiates payment on BookMyShow.

Responsibilities:
    - Navigate to the payment page.
    - Trigger the payment flow.

Does NOT:
    - Process payment (that is the payment gateway's responsibility).
    - Import Playwright.
    - Contain page selectors (pending real-selector implementation).
"""

from __future__ import annotations

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class InitiatePaymentStep(BaseBookMyShowStep):
    """
    Workflow step: initiate the payment process.

    TODO: Implement with real BookMyShow selectors in the plugin completion phase.
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
        raise NotImplementedError(
            "InitiatePaymentStep.perform() requires real BookMyShow selectors. "
            "Implement in the plugin completion phase."
        )