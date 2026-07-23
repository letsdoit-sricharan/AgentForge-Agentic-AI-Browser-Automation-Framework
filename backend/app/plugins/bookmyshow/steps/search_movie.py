"""
Purpose:
    Workflow step that searches for a movie by name on BookMyShow.

Responsibilities:
    - Type the movie name into the search box.
    - Select the matching movie from search results.
    - Verify selection succeeded.

Does NOT:
    - Import Playwright.
    - Perform browser automation directly.
    - Contain page selectors.
"""

from __future__ import annotations

from app.plugin_framework.workflow.workflow_context import WorkflowContext

from app.plugins.bookmyshow.models.booking_request import BookingRequest
from app.plugins.bookmyshow.pages.movie_page import MoviePage
from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class SearchMovieStep(BaseBookMyShowStep):
    """
    Workflow step: search for a movie by name and select it from results.
    """

    @property
    def name(self) -> str:
        return "search_movie"

    @property
    def success_message(self) -> str:
        return "Movie found and selected successfully."

    async def perform(
        self,
        context: WorkflowContext,
    ) -> None:

        request: BookingRequest = context.input_data[
            "booking_request"
        ]

        page = MoviePage(context)

        await page.search_movie(
            request.movie,
        )

        await page.select_movie(
            request.movie,
        )

        if not await page.verify_movie_selected(
            request.movie,
        ):
            raise RuntimeError(
                f"Unable to select movie '{request.movie}'."
            )