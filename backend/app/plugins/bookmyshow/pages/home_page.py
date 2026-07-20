"""
Purpose:
    Defines the UI contract for the BookMyShow home page.

Responsibilities:
    - Store homepage URL.
    - Define reusable locator constants.
    - Provide a centralized source for homepage selectors.

Does NOT:
    - Perform browser automation.
    - Import Playwright.
    - Execute browser actions.
"""

from __future__ import annotations

from typing import ClassVar

from app.plugins.bookmyshow.pages.base_page import PageLocators


class HomePage(PageLocators):
    """
    BookMyShow home page definitions.
    """

    URL: ClassVar[str] = "https://in.bookmyshow.com"

    # Navigation
    SIGN_IN_BUTTON: ClassVar[str] = "sign_in_button"
    CITY_SELECTOR: ClassVar[str] = "city_selector"

    # Search
    SEARCH_BOX: ClassVar[str] = "search_box"
    SEARCH_RESULTS: ClassVar[str] = "search_results"

    # Common
    HEADER: ClassVar[str] = "header"
    FOOTER: ClassVar[str] = "footer"