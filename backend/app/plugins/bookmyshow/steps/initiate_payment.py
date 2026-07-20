from __future__ import annotations

from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class InitiatePaymentStep(BaseBookMyShowStep):

    @property
    def name(self) -> str:
        return "initiate_payment"

    @property
    def success_message(self) -> str:
        return "Payment initiated successfully."