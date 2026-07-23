"""
Purpose:
    Workflow step that selects seats on BookMyShow.

Responsibilities:
    - Select the required number of tickets.
    - Select available seats from the canvas seat map.

Does NOT:
    - Import Playwright.
    - Contain page selectors.
"""

from __future__ import annotations

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.bookmyshow.models.booking_request import BookingRequest
from app.plugins.bookmyshow.pages.seat_page import SeatPage
from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class ChooseSeatsStep(BaseBookMyShowStep):
    """
    Workflow step: select ticket count and choose seats in the theatre.
    """

    @property
    def name(self) -> str:
        return "choose_seats"

    @property
    def success_message(self) -> str:
        return "Seats selected successfully."

    async def perform(
        self,
        context: WorkflowContext,
    ) -> None:
        request: BookingRequest = context.input_data["booking_request"]
        page = SeatPage(context)
        await page.select_ticket_count(request.ticket_count)
        await page.select_seats(
            request.ticket_count,
            preference=request.seat_preference,
        )