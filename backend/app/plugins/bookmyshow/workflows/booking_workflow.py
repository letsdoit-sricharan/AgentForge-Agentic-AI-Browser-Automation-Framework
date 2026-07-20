"""
Purpose:
    Implements the BookMyShow booking workflow.

Responsibilities:
    - Validate booking requests.
    - Execute workflow steps in order.
    - Stop on validation or step failures.
    - Return a WorkflowResult.

Does NOT:
    - Perform browser automation.
    - Import Playwright.
    - Contain page selectors.
"""

from __future__ import annotations

from app.plugin_framework.workflow.workflow import Workflow
from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugin_framework.workflow.workflow_result import WorkflowResult

from app.plugins.bookmyshow.models.booking_request import BookingRequest
from app.plugins.bookmyshow.steps.choose_date import ChooseDateStep
from app.plugins.bookmyshow.steps.choose_seats import ChooseSeatsStep
from app.plugins.bookmyshow.steps.choose_show import ChooseShowStep
from app.plugins.bookmyshow.steps.choose_theatre import ChooseTheatreStep
from app.plugins.bookmyshow.steps.download_ticket import DownloadTicketStep
from app.plugins.bookmyshow.steps.initiate_payment import InitiatePaymentStep
from app.plugins.bookmyshow.steps.open_homepage import OpenHomepageStep
from app.plugins.bookmyshow.steps.search_movie import SearchMovieStep
from app.plugins.bookmyshow.steps.select_city import SelectCityStep
from app.plugins.bookmyshow.steps.select_movie import SelectMovieStep
from app.plugins.bookmyshow.validators.booking_validator import BookingValidator


class BookingWorkflow(Workflow):
    """
    Executes the complete BookMyShow booking workflow.
    """

    def __init__(self) -> None:
        super().__init__()

        self._validator = BookingValidator()

        self.add_step(OpenHomepageStep())
        self.add_step(SelectCityStep())
        self.add_step(SearchMovieStep())
        self.add_step(SelectMovieStep())
        self.add_step(ChooseDateStep())
        self.add_step(ChooseTheatreStep())
        self.add_step(ChooseShowStep())
        self.add_step(ChooseSeatsStep())
        self.add_step(InitiatePaymentStep())
        self.add_step(DownloadTicketStep())

    @property
    def name(self) -> str:
        return "booking_workflow"

    async def execute(
    self,
    context: WorkflowContext,
    ) -> WorkflowResult:
        """
        Execute the booking workflow.
        """

        request = context.input_data.get("booking_request")

        if not isinstance(request, BookingRequest):
            return WorkflowResult(
                success=False,
                message="Booking request not found.",
            )

        validation = self._validator.validate(request)

        if not validation.valid:
            return WorkflowResult(
            success=False,
            message=validation.message,
            )

        for step in self.steps:

            result = await step.execute(context)

            if not result.success:
                return WorkflowResult(
                    success=False,
                    message=(
                    f"Workflow failed at step "
                    f"'{step.name}': {result.message}"
                ),
            )

        return WorkflowResult(
            success=True,
            message="Booking workflow completed successfully.",
        )