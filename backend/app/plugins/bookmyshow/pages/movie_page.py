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

    GLOBAL_SEARCH_BUTTON = 'div[aria-label^="Search for Movies"]'
    
    GLOBAL_SEARCH_BOX = '#search input[type="text"]'

    MOVIE_RESULT_TEMPLATE = "text={}"
    
    BOOK_TICKETS_BUTTON = "text=Book tickets"

    async def search_movie(
        self,
        movie: str,
    ) -> None:
        """
        Search for a movie.
        """
        # First click the search button if it exists
        if self.GLOBAL_SEARCH_BUTTON:
            search_btn = self.page.locator(self.GLOBAL_SEARCH_BUTTON)
            await ClickAction(locator=search_btn).execute(self.page)

        search_box = self.page.locator(
            self.GLOBAL_SEARCH_BOX,
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
        selector = self.MOVIE_RESULT_TEMPLATE.format(movie)
        
        movie_locator = self.page.locator(
            selector,
        ).first()

        await movie_locator.wait()

        await ClickAction(
            locator=movie_locator,
        ).execute(
            self.page,
        )

    async def click_book_tickets(self) -> None:
        """
        Click the Book tickets button.
        """
        if self.BOOK_TICKETS_BUTTON:
            book_btn = self.page.locator(self.BOOK_TICKETS_BUTTON).first()
            await book_btn.wait(timeout=5000)
            await ClickAction(
                locator=book_btn,
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
            # We can also verify if the BOOK_TICKETS_BUTTON is visible
            if self.BOOK_TICKETS_BUTTON:
                book_btn = self.page.locator(self.BOOK_TICKETS_BUTTON).first()
                await book_btn.wait(timeout=5000)
                return await book_btn.is_visible()

            return movie.lower() in self.page.url.lower()

        except Exception:
            return False