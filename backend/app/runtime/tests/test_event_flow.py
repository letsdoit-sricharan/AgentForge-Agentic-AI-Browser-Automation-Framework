"""
Integration test for the runtime event system.

This test verifies the complete event flow:

RuntimeEvent
        ↓
BrowserEvent
        ↓
WorkflowEvent
        ↓
EventBus
        ↓
EventHandler
"""

from app.runtime.events import (
    BrowserEvent,
    BrowserEventType,
    EventBus,
    EventHandler,
    RuntimeEvent,
    RuntimeEventType,
    WorkflowEvent,
    WorkflowEventType,
)


class PrintHandler(EventHandler):

    def __init__(self):
        self.received = []

    def handle(self, event):

        self.received.append(event)

        print(f"Received -> {event.name}")


def test_event_flow():

    print("\n==============================")
    print(" Event Flow Test ")
    print("==============================\n")

    bus = EventBus()

    handler = PrintHandler()

    bus.subscribe(handler)

    runtime_event = RuntimeEvent(
        event_type=RuntimeEventType.STARTED,
        execution_id="exec-001",
        source="ExecutionEngine",
    )

    browser_event = BrowserEvent(
        event_type=BrowserEventType.PAGE_CREATED,
        execution_id="exec-001",
        source="BrowserExecutor",
        session_id="session-001",
        page_id="page-001",
    )

    workflow_event = WorkflowEvent(
        event_type=WorkflowEventType.TASK_COMPLETED,
        execution_id="exec-001",
        workflow_id="book_ticket",
        source="WorkflowExecutor",
        task_name="Select Movie",
    )

    print("Publishing Runtime Event...")
    bus.publish(runtime_event)

    print("Publishing Browser Event...")
    bus.publish(browser_event)

    print("Publishing Workflow Event...")
    bus.publish(workflow_event)

    print()

    print(f"Total Events Received : {len(handler.received)}")

    assert len(handler.received) == 3

    assert isinstance(handler.received[0], RuntimeEvent)
    assert isinstance(handler.received[1], BrowserEvent)
    assert isinstance(handler.received[2], WorkflowEvent)

    assert handler.received[0].event_type == RuntimeEventType.STARTED

    assert handler.received[1].event_type == BrowserEventType.PAGE_CREATED

    assert handler.received[2].event_type == WorkflowEventType.TASK_COMPLETED

    print()

    print("✅ Event ordering verified.")

    print("✅ Event dispatch verified.")

    print("✅ Event Flow Test Passed!")


if __name__ == "__main__":
    test_event_flow()
