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
from app.runtime.events.global_bus import global_bus
from app.runtime.events.workflow_event import WorkflowEvent
from app.runtime.events.event_types import WorkflowEventType
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
        exec_id = context.input_data.get("request_id", "unknown")

        def emit(event_type: WorkflowEventType, task_name: str | None = None, message: str | None = None):
            payload = {"plugin_name": "BookMyShow"}
            if message:
                payload["message"] = message
            global_bus.publish(WorkflowEvent(
                event_type=event_type,
                execution_id=exec_id,
                workflow_id=self.name,
                source="booking_workflow",
                task_name=task_name,
                payload=payload
            ))

        emit(WorkflowEventType.WORKFLOW_STARTED)

        if not isinstance(request, BookingRequest):
            emit(WorkflowEventType.WORKFLOW_FAILED, message="Booking request not found.")
            return WorkflowResult(
                success=False,
                message="Booking request not found.",
            )

        validation = self._validator.validate(request)

        if not validation.valid:
            emit(WorkflowEventType.WORKFLOW_FAILED, message=validation.message)
            return WorkflowResult(
                success=False,
                message=validation.message,
            )

        for step in self.steps:
            emit(WorkflowEventType.TASK_STARTED, task_name=step.name)
            result = await step.execute(context)

            if not result.success:
                emit(WorkflowEventType.TASK_FAILED, task_name=step.name, message=result.message)
                msg = f"Workflow failed at step '{step.name}': {result.message}"
                emit(WorkflowEventType.WORKFLOW_FAILED, message=msg)
                return WorkflowResult(
                    success=False,
                    message=msg,
                )
            
            emit(WorkflowEventType.TASK_COMPLETED, task_name=step.name)

        emit(WorkflowEventType.WORKFLOW_COMPLETED, message="Booking workflow completed successfully.")
        return WorkflowResult(
            success=True,
            message="Booking workflow completed successfully.",
        )
