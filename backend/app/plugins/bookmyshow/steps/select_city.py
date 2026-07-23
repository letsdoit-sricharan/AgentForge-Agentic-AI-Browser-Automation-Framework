from __future__ import annotations

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.bookmyshow.models.booking_request import BookingRequest
from app.plugins.bookmyshow.pages.home_page import HomePage
from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class SelectCityStep(BaseBookMyShowStep):

    @property
    def name(self) -> str:
        return "select_city"

    @property
    def success_message(self) -> str:
        return "City selected successfully."

    async def perform(
        self,
        context: WorkflowContext,
    ) -> None:

        request: BookingRequest = context.input_data[
            "booking_request"
        ]

        home = HomePage(context)

        await home.search_city(
            request.city,
        )

        await home.select_city(
            request.city,
        )

        if not await home.verify_city_selected(
            request.city,
        ):
            raise RuntimeError(
                f"Unable to select city '{request.city}'."
            )
