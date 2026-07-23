"""
Tests for EventBus.
"""

from app.runtime.events.event_bus import EventBus
from app.runtime.events.event_handlers import EventHandler
from app.runtime.events.event_types import RuntimeEventType
from app.runtime.events.runtime_event import RuntimeEvent


class PrintHandler(EventHandler):
    """Simple handler used for testing."""

    def handle(self, event):

        print(f"Received -> {event.name}")


def test_event_bus():

    print("\n==============================")
    print(" Event Bus Test ")
    print("==============================\n")

    bus = EventBus()

    handler = PrintHandler()

    bus.subscribe(handler)

    print(f"Handlers Registered : {bus.handler_count}")

    event = RuntimeEvent(
        event_type=RuntimeEventType.STARTED,
        execution_id="exec-001",
        source="ExecutionEngine",
    )

    print("\nPublishing Event...\n")

    bus.publish(event)

    assert bus.handler_count == 1
    assert bus.has_handlers

    bus.unsubscribe(handler)

    assert bus.handler_count == 0

    print("\nHandler removed successfully.")

    print("\n✅ Event Bus Test Passed!")


if __name__ == "__main__":
    test_event_bus()
