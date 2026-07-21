"""
Integration test for BookingWorkflow.

Run:

python -m app.plugins.bookmyshow.tests.test_booking_workflow
"""

from __future__ import annotations

import asyncio
from datetime import date

from app.browser_engine.managers.browser_manager import BrowserManager
from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.bookmyshow.models.booking_request import BookingRequest
from app.plugins.bookmyshow.workflows.booking_workflow import BookingWorkflow
from app.plugins.interfaces.plugin_context import PluginContext


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

        booking_request = BookingRequest(
            city="Chennai",
            movie="Coolie",
            show_date=date(2026, 8, 15),
            ticket_count=2,
        )

        context = WorkflowContext(
            plugin_context=plugin_context,
            page=page,
            session=session.session,
            input_data={
                "booking_request": booking_request,
            },
        )

        workflow = BookingWorkflow()

        result = await workflow.execute(context)

        print(result.message)

        assert result.success is True

        print("✓ BookingWorkflow integration test passed.")

    finally:
        await browser.stop()


async def run_tests() -> None:

    print("\n" + "=" * 65)
    print("BookingWorkflow Integration Test")
    print("=" * 65)

    await test_execute()

    print("-" * 65)
    print("✅ BookingWorkflow integration test passed!")
    print("=" * 65)


if __name__ == "__main__":
    asyncio.run(run_tests())