"""
Purpose:
    Workflow step that selects a theatre on BookMyShow.

Responsibilities:
    - Select the preferred theatre and show time.

Does NOT:
    - Import Playwright.
    - Contain page selectors.
"""

from __future__ import annotations

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.bookmyshow.models.booking_request import BookingRequest
from app.plugins.bookmyshow.pages.theatre_page import TheatrePage
from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep

_DEFAULT_THEATRE = "PVR: Phoenix Palladium"
_DEFAULT_TIME = "07:30 PM"


class ChooseTheatreStep(BaseBookMyShowStep):
    """
    Workflow step: select the preferred theatre from the listing.
    """

    @property
    def name(self) -> str:
        return "choose_theatre"

    @property
    def success_message(self) -> str:
        return "Theatre selected successfully."

    async def perform(
        self,
        context: WorkflowContext,
    ) -> None:
        request: BookingRequest = context.input_data["booking_request"]
        theatre = request.preferred_theatre or _DEFAULT_THEATRE
        time = request.preferred_time or _DEFAULT_TIME
        page = TheatrePage(context)
        await page.select_theatre_and_show(theatre, time)