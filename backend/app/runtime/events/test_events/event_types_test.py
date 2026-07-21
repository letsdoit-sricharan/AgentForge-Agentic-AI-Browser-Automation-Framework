"""
Tests for event type definitions.
"""

from app.runtime.events.event_types import (
    EventCategory,
    RuntimeEventType,
    BrowserEventType,
    WorkflowEventType,
)


def test_event_types():

    print("\n==============================")
    print(" Event Types Test ")
    print("==============================\n")

    print("Categories")
    for category in EventCategory:
        print(f"  • {category.value}")

    print("\nRuntime Events")
    for event in RuntimeEventType:
        print(f"  • {event.value}")

    print("\nBrowser Events")
    for event in BrowserEventType:
        print(f"  • {event.value}")

    print("\nWorkflow Events")
    for event in WorkflowEventType:
        print(f"  • {event.value}")

    print("\n✅ Event Types Test Passed!")


if __name__ == "__main__":
    test_event_types()
