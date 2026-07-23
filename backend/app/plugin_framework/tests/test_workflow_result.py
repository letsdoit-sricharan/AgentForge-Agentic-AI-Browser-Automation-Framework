"""
Tests for WorkflowResult.

Run:
    python -m app.plugin_framework.tests.test_workflow_result
"""

from app.plugin_framework.workflow import WorkflowResult


def test_successful_result() -> None:
    """
    Test a successful workflow result.
    """

    result = WorkflowResult(
        success=True,
        message="Workflow completed successfully.",
        data={
            "booking_id": "BMS123",
            "movie": "Coolie",
        },
    )

    assert result.success is True
    assert result.message == "Workflow completed successfully."
    assert result.data["booking_id"] == "BMS123"
    assert result.data["movie"] == "Coolie"
    assert result.error is None

    print("✓ Successful WorkflowResult test passed.")


def test_failed_result() -> None:
    """
    Test a failed workflow result.
    """

    error = RuntimeError("Booking failed.")

    result = WorkflowResult(
        success=False,
        message="Workflow failed.",
        error=error,
    )

    assert result.success is False
    assert result.message == "Workflow failed."
    assert result.error is error
    assert result.data == {}

    print("✓ Failed WorkflowResult test passed.")


def test_default_values() -> None:
    """
    Test default field values.
    """

    result = WorkflowResult(success=True)

    assert result.message == ""
    assert result.data == {}
    assert result.error is None

    print("✓ WorkflowResult default values test passed.")


def run_tests() -> None:

    print("\n" + "=" * 65)
    print("WorkflowResult Tests")
    print("=" * 65)

    test_successful_result()
    test_failed_result()
    test_default_values()

    print("-" * 65)
    print("✅ All WorkflowResult tests passed!")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()
