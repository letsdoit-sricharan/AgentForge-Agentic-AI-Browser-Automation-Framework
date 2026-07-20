"""
Purpose:
    Defines the UI contract for the BookMyShow movie page.

Responsibilities:
    - Store locator constants for movie search and selection.
    - Provide a centralized source for movie page selectors.

Does NOT:
    - Perform browser automation.
    - Import Playwright.
    - Execute browser actions.
"""

from __future__ import annotations

from typing import ClassVar

from app.plugins.bookmyshow.pages.base_page import PageLocators


class MoviePage(PageLocators):
    """
    BookMyShow movie page definitions.
    """

    URL: ClassVar[str] = ""

    # Search
    SEARCH_BOX: ClassVar[str] = "search_box"
    SEARCH_RESULTS: ClassVar[str] = "search_results"

    # Movie listings
    MOVIE_CARD: ClassVar[str] = "movie_card"
    MOVIE_TITLE: ClassVar[str] = "movie_title"
    MOVIE_POSTER: ClassVar[str] = "movie_poster"

    # Show dates
    DATE_SELECTOR: ClassVar[str] = "date_selector"
    AVAILABLE_DATES: ClassVar[str] = "available_dates"

    # Continue
    BOOK_TICKETS_BUTTON: ClassVar[str] = "book_tickets_button"