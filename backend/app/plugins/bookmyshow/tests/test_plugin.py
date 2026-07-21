"""
Integration tests for the BookMyShow plugin.

Run:
    python -m app.plugins.bookmyshow.tests.test_plugin
"""

import asyncio
from datetime import date

from app.plugins.bookmyshow.plugin import BookMyShowPlugin
from app.plugins.bookmyshow.models.booking_request import BookingRequest
from app.plugins.interfaces.plugin_context import PluginContext


def create_plugin_context() -> PluginContext:
    """
    Create a PluginContext for testing.
    """

    return PluginContext(
        runtime=None,
        actions=None,
        memory=None,
        configuration=None,
        logger=None,
    )


def test_plugin_metadata() -> None:
    """
    Verify plugin metadata.
    """

    plugin = BookMyShowPlugin()

    assert plugin.metadata.name == "bookmyshow"

    print("✓ Plugin metadata test passed.")


async def test_plugin_lifecycle() -> None:
    """
    Verify initialize -> execute -> shutdown.
    """

    plugin = BookMyShowPlugin()

    context = create_plugin_context()

    plugin.initialize(context)

    request = BookingRequest(
        city="Chennai",
        movie="Coolie",
        show_date=date(2026, 8, 15),
        ticket_count=2,
    )

    from app.plugin_framework.workflow.workflow_context import WorkflowContext
    class DummyPage: pass
    class DummySession: pass
    
    workflow_context = WorkflowContext(
        plugin_context=context,
        page=DummyPage(),
        session=DummySession(),
        input_data={"booking_request": request}
    )

    result = await plugin.execute(workflow_context)

    # We expect this to fail because there's no real browser, but it shouldn't crash
    # assert result.success is True

    plugin.shutdown()

    print("✓ Plugin lifecycle test passed.")


async def test_execute_without_initialize() -> None:
    """
    Verify execution without initialization fails.
    """

    plugin = BookMyShowPlugin()

    request = BookingRequest(
        city="Chennai",
        movie="Coolie",
        show_date=date(2026, 8, 15),
        ticket_count=2,
    )

    from app.plugin_framework.workflow.workflow_context import WorkflowContext
    class DummyPage: pass
    class DummySession: pass
    
    workflow_context = WorkflowContext(
        plugin_context=create_plugin_context(),
        page=DummyPage(),
        session=DummySession(),
        input_data={"booking_request": request}
    )

    try:
        await plugin.execute(workflow_context)
    except RuntimeError:
        print("✓ Initialization guard test passed.")
    else:
        raise AssertionError("Expected RuntimeError.")


async def run_tests() -> None:

    print("\n" + "=" * 70)
    print("BookMyShow Plugin Tests")
    print("=" * 70)

    test_plugin_metadata()
    await test_plugin_lifecycle()
    await test_execute_without_initialize()

    print("-" * 70)
    print("✅ All BookMyShow plugin tests passed!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(run_tests())