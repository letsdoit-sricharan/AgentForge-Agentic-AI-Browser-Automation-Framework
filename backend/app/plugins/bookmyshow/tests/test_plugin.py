"""
Integration tests for the BookMyShow plugin.
"""

import asyncio
from datetime import date

import pytest

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.bookmyshow.models.booking_request import BookingRequest
from app.plugins.bookmyshow.plugin import BookMyShowPlugin
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
    """Verify plugin metadata is correctly set."""
    plugin = BookMyShowPlugin()
    assert plugin.metadata.name == "bookmyshow"


class _DummyPage:
    pass


class _DummySession:
    pass


def _make_booking_request() -> BookingRequest:
    return BookingRequest(
        city="Chennai",
        movie="Coolie",
        show_date=date(2026, 8, 15),
        ticket_count=2,
    )


async def test_plugin_lifecycle() -> None:
    """Verify initialize -> execute -> shutdown lifecycle."""
    plugin = BookMyShowPlugin()
    context = create_plugin_context()
    plugin.initialize(context)

    workflow_context = WorkflowContext(
        plugin_context=context,
        page=_DummyPage(),
        session=_DummySession(),
        input_data={"booking_request": _make_booking_request()},
    )

    _result = await plugin.execute(workflow_context)
    # We expect this to fail because there's no real browser, but it shouldn't crash
    plugin.shutdown()


async def test_execute_without_initialize() -> None:
    """Verify that executing without initialization raises RuntimeError."""
    plugin = BookMyShowPlugin()

    workflow_context = WorkflowContext(
        plugin_context=create_plugin_context(),
        page=_DummyPage(),
        session=_DummySession(),
        input_data={"booking_request": _make_booking_request()},
    )

    with pytest.raises(RuntimeError):
        await plugin.execute(workflow_context)


if __name__ == "__main__":
    asyncio.run(test_plugin_lifecycle())
