"""
Purpose:
    Defines the UI contract for the BookMyShow city selection page.

Responsibilities:
    - Store locator constants for city selection.
    - Provide a centralized source for city page selectors.

Does NOT:
    - Perform browser automation.
    - Import Playwright.
    - Execute browser actions.
"""

from __future__ import annotations

from typing import ClassVar

from app.plugins.bookmyshow.pages.base_page import PageLocators


class CityPage(PageLocators):
    """
    BookMyShow city selection page definitions.
    """

    URL: ClassVar[str] = ""

    # Search
    CITY_SEARCH_BOX: ClassVar[str] = "city_search_box"

    # Results
    CITY_RESULTS: ClassVar[str] = "city_results"
    CITY_CARD: ClassVar[str] = "city_card"

    # Recently searched / popular cities
    POPULAR_CITIES: ClassVar[str] = "popular_cities"
    RECENT_CITIES: ClassVar[str] = "recent_cities"

    # Confirmation
    CONFIRM_BUTTON: ClassVar[str] = "confirm_button"