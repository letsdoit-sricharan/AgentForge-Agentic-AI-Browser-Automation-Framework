"""
Tests for WorkflowEvent.
"""

from app.runtime.events.workflow_event import WorkflowEvent
from app.runtime.events.event_types import WorkflowEventType


def test_workflow_event():

    print("\n==============================")
    print(" Workflow Event Test ")
    print("==============================\n")

    event = WorkflowEvent(
        event_type=WorkflowEventType.TASK_COMPLETED,
        execution_id="exec-001",
        workflow_id="book_ticket",
        source="WorkflowExecutor",
        task_name="select_movie",
        payload={
            "movie": "Coolie",
            "duration": 2.4,
        },
    )

    print(f"Event ID     : {event.event_id}")
    print(f"Event Type   : {event.name}")
    print(f"Execution ID : {event.execution_id}")
    print(f"Workflow ID  : {event.workflow_id}")
    print(f"Task Name    : {event.task_name}")
    print(f"Source       : {event.source}")
    print(f"Timestamp    : {event.timestamp}")
    print(f"Payload      : {event.payload}")

    assert event.event_type == WorkflowEventType.TASK_COMPLETED
    assert event.workflow_id == "book_ticket"
    assert event.task_name == "select_movie"
    assert event.payload["movie"] == "Coolie"

    print("\n✅ Workflow Event Test Passed!")


if __name__ == "__main__":
    test_workflow_event()