"""
Tests for RuntimeEvent.
"""

from app.runtime.events.runtime_event import RuntimeEvent
from app.runtime.events.event_types import RuntimeEventType


def test_runtime_event():

    print("\n==============================")
    print(" Runtime Event Test ")
    print("==============================\n")

    event = RuntimeEvent(
        event_type=RuntimeEventType.STARTED,
        execution_id="exec-001",
        source="ExecutionEngine",
        payload={
            "workflow": "book_ticket",
            "movie": "Coolie",
        },
    )

    print(f"Event ID     : {event.event_id}")
    print(f"Event Type   : {event.name}")
    print(f"Execution ID : {event.execution_id}")
    print(f"Source       : {event.source}")
    print(f"Timestamp    : {event.timestamp}")
    print(f"Payload      : {event.payload}")

    assert event.event_type == RuntimeEventType.STARTED
    assert event.execution_id == "exec-001"
    assert event.payload["movie"] == "Coolie"

    print("\n✅ Runtime Event Test Passed!")


if __name__ == "__main__":
    test_runtime_event()
