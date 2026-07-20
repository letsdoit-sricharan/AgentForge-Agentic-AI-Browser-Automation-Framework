"""
Tests for OpenHomepageStep.

Run:
    python -m app.plugins.bookmyshow.tests.test_open_homepage_step
"""

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.interfaces.plugin_context import PluginContext
from app.plugins.bookmyshow.steps.open_homepage import OpenHomepageStep


def test_execute() -> None:
    """
    Test executing the OpenHomepageStep.
    """

    step = OpenHomepageStep()

    plugin_context = PluginContext(
        runtime=None,
        actions=None,
        memory=None,
        configuration=None,
        logger=None,
    )

    context = WorkflowContext(
        plugin_context=plugin_context,
    )

    result = step.execute(context)

    assert result.success is True
    assert "homepage" in result.message.lower()

    print("✓ OpenHomepageStep execution test passed.")


def run_tests() -> None:
    """
    Run all OpenHomepageStep tests.
    """

    print("\n" + "=" * 65)
    print("OpenHomepageStep Tests")
    print("=" * 65)

    test_execute()

    print("-" * 65)
    print("✅ All OpenHomepageStep tests passed!")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()