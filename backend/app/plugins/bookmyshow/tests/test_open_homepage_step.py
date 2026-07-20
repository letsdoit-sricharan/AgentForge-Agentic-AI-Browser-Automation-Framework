"""
Tests for OpenHomepageStep.

Run:
    python -m app.plugins.bookmyshow.tests.test_open_homepage_step
"""

from __future__ import annotations

import asyncio

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.bookmyshow.steps.open_homepage import OpenHomepageStep
from app.plugins.interfaces.plugin_context import PluginContext


class DummyLocator:
    async def wait(self, timeout=None):
        return None

    async def is_visible(self):
        return True


class DummyPage:
    async def goto(self, *args, **kwargs):
        return None

    async def wait_for_load(self, *args, **kwargs):
        return None

    def locator(self, selector):
        return DummyLocator()

    async def title(self):
        return "BookMyShow"

    @property
    def url(self):
        return "https://in.bookmyshow.com/explore/home"


class DummySession:
    pass


async def test_execute():

    plugin_context = PluginContext(
        runtime=None,
        actions=None,
        memory=None,
        configuration=None,
        logger=None,
    )

    context = WorkflowContext(
        plugin_context=plugin_context,
        page=DummyPage(),
        session=DummySession(),
    )

    step = OpenHomepageStep()

    result = await step.execute(context)

    assert result.success
    print("✓ OpenHomepageStep execution test passed.")


async def run_tests():

    print("\n" + "=" * 65)
    print("OpenHomepageStep Tests")
    print("=" * 65)

    await test_execute()

    print("-" * 65)
    print("✅ All OpenHomepageStep tests passed!")
    print("=" * 65)


if __name__ == "__main__":
    asyncio.run(run_tests())