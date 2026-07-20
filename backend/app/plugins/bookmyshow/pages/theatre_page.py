"""
Purpose:
    Defines the UI contract for the BookMyShow theatre selection page.

Responsibilities:
    - Store locator constants for theatre and show selection.
    - Provide a centralized source for theatre page selectors.

Does NOT:
    - Perform browser automation.
    - Import Playwright.
    - Execute browser actions.
"""

from __future__ import annotations

from typing import ClassVar

from app.plugins.bookmyshow.pages.base_page import PageLocators


class TheatrePage(PageLocators):
    """
    BookMyShow theatre page definitions.
    """

    URL: ClassVar[str] = ""

    # Theatre listings
    THEATRE_LIST: ClassVar[str] = "theatre_list"
    THEATRE_CARD: ClassVar[str] = "theatre_card"
    THEATRE_NAME: ClassVar[str] = "theatre_name"

    # Show timings
    SHOW_LIST: ClassVar[str] = "show_list"
    SHOW_TIME: ClassVar[str] = "show_time"

    # Availability
    AVAILABLE_SHOW: ClassVar[str] = "available_show"
    FAST_FILLING_BADGE: ClassVar[str] = "fast_filling_badge"
    SOLD_OUT_BADGE: ClassVar[str] = "sold_out_badge"

    # Navigation
    NEXT_BUTTON: ClassVar[str] = "next_button"