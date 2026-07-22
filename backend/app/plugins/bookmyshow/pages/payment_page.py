"""
Purpose:
    Represents the BookMyShow payment page.

Responsibilities:
    - Enter contact details.
    - Proceed to payment.
    - Download ticket (if applicable).

Does NOT:
    - Execute workflow logic.
    - Import Playwright.
"""

from __future__ import annotations

from app.actions.element import ClickAction, FillAction
from app.plugin_framework.pages import BasePage


class PaymentPage(BasePage):
    """
    Page Object representing the payment page/modal.
    """

    EMAIL_INPUT = 'input[id="deemed-email"]'

    PHONE_INPUT = 'input[id="deemed-mobile-number"]'

    CONTINUE_PAYMENT_BUTTON = "role=button[name='Submit'i]"

    DOWNLOAD_TICKET_BUTTON = "text=Download Ticket"

    async def enter_contact_details(self, email: str, phone: str) -> None:
        """
        Enter contact details to proceed with payment.
        """
        email_locator = self.page.locator(self.EMAIL_INPUT)
        await email_locator.wait()
        await FillAction(locator=email_locator, text=email).execute(self.page)

        phone_locator = self.page.locator(self.PHONE_INPUT)
        await FillAction(locator=phone_locator, text=phone).execute(self.page)

    async def proceed_to_payment(self) -> None:
        """
        Click the button to continue to the payment gateway.
        """
        btn_locator = self.page.locator(self.CONTINUE_PAYMENT_BUTTON)
        await ClickAction(locator=btn_locator).execute(self.page)

    async def download_ticket(self) -> None:
        """
        Click the download ticket button on the confirmation page.
        """
        btn_locator = self.page.locator(self.DOWNLOAD_TICKET_BUTTON)
        await btn_locator.wait()
        await ClickAction(locator=btn_locator).execute(self.page)