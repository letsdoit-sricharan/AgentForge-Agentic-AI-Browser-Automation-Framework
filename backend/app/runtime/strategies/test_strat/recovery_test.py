"""
Tests for RecoveryStrategy.
"""

from app.runtime.execution.execution_context import ExecutionContext
from app.runtime.execution.execution_metadata import ExecutionMetadata
from app.runtime.execution.execution_request import ExecutionRequest
from app.runtime.memory.runtime_memory import RuntimeMemory
from app.runtime.state.execution_state import ExecutionState
from app.runtime.state.execution_status import ExecutionStatus
from app.runtime.state.workflow_state import WorkflowState
from app.runtime.strategies.recovery_strategy import (
    RecoveryStrategy,
)


def create_context() -> ExecutionContext:
    context = ExecutionContext(
        request=ExecutionRequest(
            plugin="bookmyshow",
            workflow="book_ticket",
        ),
        metadata=ExecutionMetadata(),
        execution_state=ExecutionState("exec-1"),
        workflow_state=WorkflowState(
            workflow_id="wf-1",
            total_steps=5,
        ),
        memory=RuntimeMemory(),
    )

    context.execution_state.status = ExecutionStatus.FAILED
    context.execution_state.retry_count = 3

    context.workflow_state.current_step = "seat_selection"
    context.workflow_state.completed_steps = 3

    context.memory.set("movie", "Coolie")

    return context


def test_recovery_strategy():
    strategy = RecoveryStrategy(
        clear_memory=True,
        reset_workflow=True,
    )

    context = create_context()

    print("\nRecovering execution...")

    strategy.recover(context)

    assert context.execution_state.status == ExecutionStatus.CREATED
    assert context.execution_state.retry_count == 0

    assert context.workflow_state.current_step is None
    assert context.workflow_state.completed_steps == 0

    assert context.memory.size == 0

    print("✅ RecoveryStrategy test passed!")


if __name__ == "__main__":
    test_recovery_strategy()