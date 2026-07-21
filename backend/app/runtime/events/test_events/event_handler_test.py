"""
Tests for EventHandler.
"""

from app.runtime.events.event_handlers import EventHandler
from app.runtime.events.runtime_event import RuntimeEvent
from app.runtime.events.event_types import RuntimeEventType


class PrintHandler(EventHandler):
    """
    Simple event handler used for testing.
    """

    def handle(self, event):

        print(f"Received Event : {event.name}")


def test_event_handler():

    print("\n==============================")
    print(" Event Handler Test ")
    print("==============================\n")

    handler = PrintHandler()

    event = RuntimeEvent(
        event_type=RuntimeEventType.STARTED,
        execution_id="exec-001",
        source="ExecutionEngine",
    )

    handler.handle(event)

    print("\n✅ Event Handler Test Passed!")


if __name__ == "__main__":
    test_event_handler()
