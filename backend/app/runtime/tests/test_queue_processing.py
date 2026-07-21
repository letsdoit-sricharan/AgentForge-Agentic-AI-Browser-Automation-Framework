"""
Queue Processing Integration Test.

Verifies that ExecutionQueue correctly processes
execution contexts in FIFO order.
"""

from app.runtime.execution.execution_context import ExecutionContext
from app.runtime.execution.execution_metadata import ExecutionMetadata
from app.runtime.execution.execution_queue import ExecutionQueue
from app.runtime.execution.execution_request import ExecutionRequest
from app.runtime.memory.runtime_memory import RuntimeMemory
from app.runtime.state.execution_state import ExecutionState
from app.runtime.state.workflow_state import WorkflowState


def create_context(workflow: str) -> ExecutionContext:
    """Create a test execution context."""

    return ExecutionContext(
        request=ExecutionRequest(
            plugin_context=None,
            plugin="bookmyshow",
            task=workflow,
        ),
        metadata=ExecutionMetadata(),
        execution_state=ExecutionState(
            execution_id="exec-1",
        ),
        workflow_state=WorkflowState(
            workflow_id=workflow,
            total_steps=1,
        ),
        memory=RuntimeMemory(),
    )


def test_queue_processing():

    print("\n==============================")
    print(" Queue Processing Test ")
    print("==============================\n")

    queue = ExecutionQueue()

    context1 = create_context("workflow_1")
    context2 = create_context("workflow_2")
    context3 = create_context("workflow_3")

    # ----------------------------
    # Enqueue
    # ----------------------------

    queue.enqueue(context1)
    print("Enqueued workflow_1")

    queue.enqueue(context2)
    print("Enqueued workflow_2")

    queue.enqueue(context3)
    print("Enqueued workflow_3")

    # ----------------------------
    # Queue Size
    # ----------------------------

    assert queue.size == 3

    print(f"Queue Size: {queue.size}")

    # ----------------------------
    # FIFO Verification
    # ----------------------------

    first = queue.dequeue()
    second = queue.dequeue()
    third = queue.dequeue()

    assert first.request.task == "workflow_1"
    assert second.request.task == "workflow_2"
    assert third.request.task == "workflow_3"

    print("\nFIFO order verified.")

    # ----------------------------
    # Queue Empty
    # ----------------------------

    assert queue.is_empty

    print("Queue is empty.")

    print("\n✅ Queue Processing Test Passed!")


if __name__ == "__main__":
    test_queue_processing()
