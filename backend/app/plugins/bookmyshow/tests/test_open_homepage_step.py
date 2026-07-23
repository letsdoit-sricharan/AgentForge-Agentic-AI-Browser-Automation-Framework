"""
Integration test for OpenHomepageStep.

Run:

python -m app.plugins.bookmyshow.tests.test_open_homepage_step
"""

from __future__ import annotations

import asyncio

import pytest

from app.browser_engine.managers.browser_manager import BrowserManager
from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.bookmyshow.steps.open_homepage import OpenHomepageStep
from app.plugins.interfaces.plugin_context import PluginContext


@pytest.mark.skip(reason="Integration test requiring browser and network access")
async def test_execute() -> None:

    browser = BrowserManager()

    await browser.start()

    try:
        session = await browser.create_session()

        page = await session.new_page()

        plugin_context = PluginContext(
            runtime=None,
            actions=None,
            memory=None,
            configuration=None,
            logger=None,
        )

        context = WorkflowContext(
            plugin_context=plugin_context,
            page=page,
            session=session.session,
        )

        step = OpenHomepageStep()

        result = await step.execute(context)

        print(result.message)

        assert result.success is True

        print("[PASS] OpenHomepageStep integration test passed.")

    finally:
        await browser.stop()


async def run_tests() -> None:

    print("\n" + "=" * 65)
    print("OpenHomepageStep Integration Test")
    print("=" * 65)

    await test_execute()

    print("-" * 65)
    print("[PASS] Integration test passed!")
    print("=" * 65)


if __name__ == "__main__":
    asyncio.run(run_tests())
