"""
Purpose:
    Workflow step that selects a show date on BookMyShow.

Responsibilities:
    - Click the Book Tickets button on the movie detail page.
    - Select the requested show date from the date filters.

Does NOT:
    - Import Playwright.
    - Contain page selectors.
"""

from __future__ import annotations

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.bookmyshow.models.booking_request import BookingRequest
from app.plugins.bookmyshow.pages.movie_page import MoviePage
from app.plugins.bookmyshow.pages.theatre_page import TheatrePage
from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class ChooseDateStep(BaseBookMyShowStep):
    """
    Workflow step: click Book Tickets then select the show date.
    """

    @property
    def name(self) -> str:
        return "choose_date"

    @property
    def success_message(self) -> str:
        return "Show date selected successfully."

    async def perform(
        self,
        context: WorkflowContext,
    ) -> None:
        request: BookingRequest = context.input_data["booking_request"]

        # Navigate from movie detail page → theatre/date listing
        movie_page = MoviePage(context)
        await movie_page.click_book_tickets()

        # Select the requested date
        theatre_page = TheatrePage(context)
        await theatre_page.select_date(str(request.show_date))
