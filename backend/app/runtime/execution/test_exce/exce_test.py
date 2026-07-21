"""
Tests for ExecutionQueue.
"""

from app.runtime.execution.execution_context import ExecutionContext
from app.runtime.execution.execution_metadata import ExecutionMetadata
from app.runtime.execution.execution_queue import ExecutionQueue
from app.runtime.execution.execution_request import ExecutionRequest
from app.runtime.memory.runtime_memory import RuntimeMemory
from app.runtime.state.execution_state import ExecutionState
from app.runtime.state.workflow_state import WorkflowState


def create_context() -> ExecutionContext:
    return ExecutionContext(
        request=ExecutionRequest(
            plugin_context=None,
            plugin="bookmyshow",
            task="book_ticket",
        ),
        metadata=ExecutionMetadata(),
        execution_state=ExecutionState("exec-1"),
        workflow_state=WorkflowState(
            workflow_id="wf-1",
            total_steps=5,
        ),
        memory=RuntimeMemory(),
    )


def test_execution_queue():
    queue = ExecutionQueue()

    print("\nCreating empty queue...")

    assert queue.is_empty
    assert queue.size == 0

    context = create_context()

    print("Enqueueing execution context...")

    queue.enqueue(context)

    assert not queue.is_empty
    assert queue.size == 1

    print("Peeking queue...")

    assert queue.peek() is context

    print("Dequeuing execution context...")

    item = queue.dequeue()

    assert item is context

    assert queue.is_empty
    assert queue.size == 0

    print("✅ ExecutionQueue test passed!")


if __name__ == "__main__":
    test_execution_queue()
