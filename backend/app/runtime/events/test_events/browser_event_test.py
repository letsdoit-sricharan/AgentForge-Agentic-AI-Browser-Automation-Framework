"""
Tests for BrowserEvent.
"""

from app.runtime.events.browser_event import BrowserEvent
from app.runtime.events.event_types import BrowserEventType


def test_browser_event():

    print("\n==============================")
    print(" Browser Event Test ")
    print("==============================\n")

    event = BrowserEvent(
        event_type=BrowserEventType.PAGE_CREATED,
        execution_id="exec-001",
        source="BrowserExecutor",
        session_id="session-101",
        page_id="page-1",
        payload={
            "url": "https://in.bookmyshow.com",
        },
    )

    print(f"Event ID     : {event.event_id}")
    print(f"Event Type   : {event.name}")
    print(f"Execution ID : {event.execution_id}")
    print(f"Session ID   : {event.session_id}")
    print(f"Page ID      : {event.page_id}")
    print(f"Source       : {event.source}")
    print(f"Timestamp    : {event.timestamp}")
    print(f"Payload      : {event.payload}")

    assert event.event_type == BrowserEventType.PAGE_CREATED
    assert event.session_id == "session-101"
    assert event.page_id == "page-1"
    assert event.payload["url"] == "https://in.bookmyshow.com"

    print("\n✅ Browser Event Test Passed!")


if __name__ == "__main__":
    test_browser_event()