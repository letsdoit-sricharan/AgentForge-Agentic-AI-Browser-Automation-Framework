"""
Tests for StepResult.

Run:
    python -m app.plugin_framework.tests.test_step_result
"""

from app.plugin_framework.steps.step_result import StepResult


def test_successful_step_result() -> None:
    """
    Test a successful step result.
    """

    result = StepResult(
        success=True,
        message="Step executed successfully.",
        data={
            "step": "SearchMovie",
            "movie": "Coolie",
        },
    )

    assert result.success is True
    assert result.message == "Step executed successfully."
    assert result.data["step"] == "SearchMovie"
    assert result.data["movie"] == "Coolie"
    assert result.error is None

    print("✓ Successful StepResult test passed.")


def test_failed_step_result() -> None:
    """
    Test a failed step result.
    """

    error = ValueError("Movie not found.")

    result = StepResult(
        success=False,
        message="Step execution failed.",
        error=error,
    )

    assert result.success is False
    assert result.message == "Step execution failed."
    assert result.error is error
    assert result.data == {}

    print("✓ Failed StepResult test passed.")


def test_default_values() -> None:
    """
    Test default field values.
    """

    result = StepResult(success=True)

    assert result.message == ""
    assert result.data == {}
    assert result.error is None

    print("✓ StepResult default values test passed.")


def run_tests() -> None:

    print("\n" + "=" * 65)
    print("StepResult Tests")
    print("=" * 65)

    test_successful_step_result()
    test_failed_step_result()
    test_default_values()

    print("-" * 65)
    print("✅ All StepResult tests passed!")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()