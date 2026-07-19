"""
Tests for WorkflowContext.

Run:
    python -m app.plugin_framework.tests.test_workflow_context
"""

from app.plugin_framework.workflow import WorkflowContext
from app.plugins.interfaces import PluginContext


def create_plugin_context() -> PluginContext:
    """
    Create a dummy PluginContext for testing.
    """
    return PluginContext(
        runtime=None,
        actions=None,
        configuration=None,
        memory=None,
        logger=None,
    )


def test_workflow_context_creation() -> None:
    """
    Test WorkflowContext initialization.
    """

    context = WorkflowContext(
        plugin_context=create_plugin_context(),
    )

    assert context.plugin_context is not None
    assert context.input_data == {}
    assert context.state == {}

    print("✓ WorkflowContext creation test passed.")


def test_input_data() -> None:
    """
    Test input data storage.
    """

    context = WorkflowContext(
        plugin_context=create_plugin_context(),
        input_data={
            "movie": "Coolie",
            "tickets": 2,
        },
    )

    assert context.input_data["movie"] == "Coolie"
    assert context.input_data["tickets"] == 2

    print("✓ WorkflowContext input data test passed.")


def test_state_storage() -> None:
    """
    Test shared workflow state.
    """

    context = WorkflowContext(
        plugin_context=create_plugin_context(),
    )

    context.state["city"] = "Chennai"
    context.state["language"] = "Telugu"

    assert context.state["city"] == "Chennai"
    assert context.state["language"] == "Telugu"

    print("✓ WorkflowContext state storage test passed.")


def run_tests() -> None:

    print("\n" + "=" * 65)
    print("WorkflowContext Tests")
    print("=" * 65)

    test_workflow_context_creation()
    test_input_data()
    test_state_storage()

    print("-" * 65)
    print("✅ All WorkflowContext tests passed!")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()