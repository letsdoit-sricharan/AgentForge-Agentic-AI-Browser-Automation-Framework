"""
Memory Persistence Integration Test.

Verifies that RuntimeMemory persists data across
multiple tasks within the same execution context.
"""

from app.runtime.execution.execution_context import ExecutionContext
from app.runtime.execution.execution_metadata import ExecutionMetadata
from app.runtime.execution.execution_request import ExecutionRequest
from app.runtime.memory.runtime_memory import RuntimeMemory
from app.runtime.state.execution_state import ExecutionState
from app.runtime.state.workflow_state import WorkflowState


def create_context() -> ExecutionContext:
    """Create a test execution context."""

    return ExecutionContext(
        request=ExecutionRequest(
            plugin="bookmyshow",
            workflow="memory_test",
        ),
        metadata=ExecutionMetadata(),
        execution_state=ExecutionState(
            execution_id="memory-test-001",
        ),
        workflow_state=WorkflowState(
            workflow_id="memory-workflow",
            total_steps=3,
        ),
        memory=RuntimeMemory(),
    )


def task_select_movie(context: ExecutionContext):
    """Simulate selecting a movie."""

    print("Task 1 -> Selecting movie...")
    context.memory.set("movie", "Coolie")


def task_select_theatre(context: ExecutionContext):
    """Read movie from memory and store theatre."""

    movie = context.memory.get("movie")

    print(f"Task 2 -> Movie from memory: {movie}")

    assert movie == "Coolie"

    context.memory.set("theatre", "PVR Cinemas")


def task_confirm(context: ExecutionContext):
    """Verify all stored values."""

    movie = context.memory.get("movie")
    theatre = context.memory.get("theatre")

    print(f"Task 3 -> Movie   : {movie}")
    print(f"Task 3 -> Theatre : {theatre}")

    assert movie == "Coolie"
    assert theatre == "PVR Cinemas"


def test_memory_persistence():

    print("\n==============================")
    print(" Memory Persistence Test ")
    print("==============================\n")

    context = create_context()

    task_select_movie(context)
    task_select_theatre(context)
    task_confirm(context)

    print("\nStored Memory")

    print("------------------------")

    print(
        "Movie   :",
        context.memory.get("movie"),
    )

    print(
        "Theatre :",
        context.memory.get("theatre"),
    )

    print("\n✅ Memory Persistence Test Passed!")


if __name__ == "__main__":
    test_memory_persistence()