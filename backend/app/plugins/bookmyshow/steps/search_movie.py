from __future__ import annotations

from app.plugin_framework.workflow.workflow_context import WorkflowContext

from app.plugins.bookmyshow.models.booking_request import BookingRequest
from app.plugins.bookmyshow.pages.movie_page import MoviePage
from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class SelectMovieStep(BaseBookMyShowStep):

    @property
    def name(self) -> str:
        return "select_movie"

    @property
    def success_message(self) -> str:
        return "Movie selected successfully."

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