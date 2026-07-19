"""
Tests for Plugin Framework exceptions.

Run:
    python -m app.plugin_framework.tests.test_workflow_errors
"""

from app.plugin_framework.exceptions import (
    StepExecutionError,
    ValidationError,
    WorkflowConfigurationError,
    WorkflowError,
    WorkflowExecutionError,
)


def test_workflow_error() -> None:
    """
    Test the base WorkflowError.
    """

    error = WorkflowError("Generic workflow error.")

    assert isinstance(error, Exception)
    assert str(error) == "Generic workflow error."

    print("✓ WorkflowError test passed.")


def test_workflow_execution_error() -> None:
    """
    Test WorkflowExecutionError.
    """

    error = WorkflowExecutionError("Workflow execution failed.")

    assert isinstance(error, WorkflowError)
    assert str(error) == "Workflow execution failed."

    print("✓ WorkflowExecutionError test passed.")


def test_step_execution_error() -> None:
    """
    Test StepExecutionError.
    """

    error = StepExecutionError("Step execution failed.")

    assert isinstance(error, WorkflowError)
    assert str(error) == "Step execution failed."

    print("✓ StepExecutionError test passed.")


def test_validation_error() -> None:
    """
    Test ValidationError.
    """

    error = ValidationError("Validation failed.")

    assert isinstance(error, WorkflowError)
    assert str(error) == "Validation failed."

    print("✓ ValidationError test passed.")


def test_workflow_configuration_error() -> None:
    """
    Test WorkflowConfigurationError.
    """

    error = WorkflowConfigurationError(
        "Workflow configuration is invalid."
    )

    assert isinstance(error, WorkflowError)
    assert str(error) == "Workflow configuration is invalid."

    print("✓ WorkflowConfigurationError test passed.")


def run_tests() -> None:

    print("\n" + "=" * 65)
    print("Workflow Exception Tests")
    print("=" * 65)

    test_workflow_error()
    test_workflow_execution_error()
    test_step_execution_error()
    test_validation_error()
    test_workflow_configuration_error()

    print("-" * 65)
    print("✅ All Workflow Exception tests passed!")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()