"""
Integration tests for BookingWorkflow.

Run:
    python -m app.plugins.bookmyshow.tests.test_booking_workflow
"""

from datetime import date

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.bookmyshow.models.booking_request import BookingRequest
from app.plugins.bookmyshow.workflows.booking_workflow import BookingWorkflow
from app.plugins.interfaces.plugin_context import PluginContext


def create_workflow_context(request: BookingRequest) -> WorkflowContext:
    """
    Create a WorkflowContext for testing.
    """

    plugin_context = PluginContext(
        runtime=None,
        actions=None,
        memory=None,
        configuration=None,
        logger=None,
    )

    return WorkflowContext(
        plugin_context=plugin_context,
        input_data={
            "booking_request": request,
        },
    )


def test_successful_booking_workflow() -> None:
    """
    Test the complete booking workflow.
    """

    request = BookingRequest(
        city="Chennai",
        movie="Coolie",
        show_date=date(2026, 8, 15),
        ticket_count=2,
    )

    workflow = BookingWorkflow()

    context = create_workflow_context(request)

    result = workflow.execute(context)

    assert result.success is True

    print("✓ BookingWorkflow execution test passed.")


def test_invalid_booking_request() -> None:
    """
    Test workflow validation failure.
    """

    request = BookingRequest(
        city="",
        movie="Coolie",
        show_date=date(2026, 8, 15),
        ticket_count=2,
    )

    workflow = BookingWorkflow()

    context = create_workflow_context(request)

    result = workflow.execute(context)

    assert result.success is False

    print("✓ BookingWorkflow validation failure test passed.")


def run_tests() -> None:

    print("\n" + "=" * 70)
    print("BookMyShow BookingWorkflow Integration Tests")
    print("=" * 70)

    test_successful_booking_workflow()
    test_invalid_booking_request()

    print("-" * 70)
    print("✅ All BookingWorkflow integration tests passed!")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()