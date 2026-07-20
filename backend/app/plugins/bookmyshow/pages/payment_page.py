"""
Purpose:
    Defines the UI contract for the BookMyShow payment page.

Responsibilities:
    - Store locator constants for payment and ticket confirmation.
    - Provide a centralized source for payment page selectors.

Does NOT:
    - Perform browser automation.
    - Import Playwright.
    - Execute browser actions.
"""

from __future__ import annotations

from typing import ClassVar

from app.plugins.bookmyshow.pages.base_page import PageLocators


class PaymentPage(PageLocators):
    """
    BookMyShow payment page definitions.
    """

    URL: ClassVar[str] = ""

    # Payment
    PAYMENT_METHODS: ClassVar[str] = "payment_methods"
    PAYMENT_BUTTON: ClassVar[str] = "payment_button"

    # Status
    PAYMENT_STATUS: ClassVar[str] = "payment_status"
    SUCCESS_MESSAGE: ClassVar[str] = "success_message"
    FAILURE_MESSAGE: ClassVar[str] = "failure_message"

    # Ticket
    DOWNLOAD_TICKET_BUTTON: ClassVar[str] = "download_ticket_button"
    BOOKING_ID: ClassVar[str] = "booking_id"

    # Navigation
    BACK_TO_HOME_BUTTON: ClassVar[str] = "back_to_home_button"