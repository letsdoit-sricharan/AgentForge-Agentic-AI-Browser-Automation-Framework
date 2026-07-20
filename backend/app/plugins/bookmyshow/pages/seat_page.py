"""
Purpose:
    Defines the UI contract for the BookMyShow seat selection page.

Responsibilities:
    - Store locator constants for seat selection.
    - Provide a centralized source for seat page selectors.

Does NOT:
    - Perform browser automation.
    - Import Playwright.
    - Execute browser actions.
"""

from __future__ import annotations

from typing import ClassVar

from app.plugins.bookmyshow.pages.base_page import PageLocators


class SeatPage(PageLocators):
    """
    BookMyShow seat selection page definitions.
    """

    URL: ClassVar[str] = ""

    # Seat layout
    SEAT_MAP: ClassVar[str] = "seat_map"
    SEAT_ROW: ClassVar[str] = "seat_row"
    SEAT: ClassVar[str] = "seat"

    # Seat states
    AVAILABLE_SEAT: ClassVar[str] = "available_seat"
    SELECTED_SEAT: ClassVar[str] = "selected_seat"
    BOOKED_SEAT: ClassVar[str] = "booked_seat"

    # Categories
    SEAT_CATEGORY: ClassVar[str] = "seat_category"

    # Booking summary
    TICKET_COUNT: ClassVar[str] = "ticket_count"
    TOTAL_PRICE: ClassVar[str] = "total_price"

    # Navigation
    PROCEED_BUTTON: ClassVar[str] = "proceed_button"