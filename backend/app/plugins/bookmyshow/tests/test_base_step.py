"""
Tests for BaseBookMyShowStep.

Run:
    python -m app.plugins.bookmyshow.tests.test_base_step
"""

from __future__ import annotations

import asyncio

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep
from app.plugins.interfaces.plugin_context import PluginContext


class DummyStep(BaseBookMyShowStep):
    """
    Dummy implementation for testing the base class.
    """

    @property
    def name(self) -> str:
        return "dummy_step"

    @property
    def success_message(self) -> str:
        return "Dummy step executed successfully."

    async def perform(self, context: WorkflowContext) -> None:
        pass


async def test_execute() -> None:
    """
    Verify the default placeholder execution.
    """

    step = DummyStep()

    plugin_context = PluginContext(
        runtime=None,
        actions=None,
        memory=None,
        configuration=None,
        logger=None,
    )

    context = WorkflowContext(
    plugin_context=plugin_context,
    page=None,
    session=None,
)

    result = await step.execute(context)

    assert result.success is True
    assert result.message == "Dummy step executed successfully."

    print("✓ BaseBookMyShowStep execution test passed.")


async def run_tests() -> None:

    print("\n" + "=" * 65)
    print("BaseBookMyShowStep Tests")
    print("=" * 65)

    await test_execute()

    print("-" * 65)
    print("✅ All BaseBookMyShowStep tests passed!")
    print("=" * 65)


if __name__ == "__main__":
    asyncio.run(run_tests())