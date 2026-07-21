"""
Purpose:
    Represents the BookMyShow movie search page.

Responsibilities:
    - Store selectors for searching and selecting movies.
    - Act as the Page Object for movie-related interactions.

Does NOT:
    - Execute workflow logic.
    - Import Playwright.
    - Perform browser automation directly.
"""

from __future__ import annotations

from app.actions.element import ClickAction, FillAction
from app.plugin_framework.pages import BasePage


class MoviePage(BasePage):
    """
    Page Object representing the movie search page.
    """

    SEARCH_BOX = 'input[placeholder*="Search"]'

    async def search_movie(
        self,
        movie: str,
    ) -> None:
        """
        Search for a movie.
        """

        search_box = self.page.locator(
            self.SEARCH_BOX,
        )

        await FillAction(
            locator=search_box,
            text=movie,
        ).execute(
            self.page,
        )

    async def select_movie(
        self,
        movie: str,
    ) -> None:
        """
        Select a movie from the search results.
        """

        movie_locator = self.page.locator(
            f"text={movie}",
        )

        await movie_locator.wait()

        await ClickAction(
            locator=movie_locator,
        ).execute(
            self.page,
        )

    async def verify_movie_selected(
        self,
        movie: str,
    ) -> bool:
        """
        Verify that the selected movie page is displayed.
        """

        try:

            return movie.lower() in self.page.url.lower()

        except Exception:
            return False