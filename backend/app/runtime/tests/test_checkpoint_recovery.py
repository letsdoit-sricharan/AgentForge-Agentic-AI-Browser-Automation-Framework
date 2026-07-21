"""
Checkpoint Recovery Integration Test.

Verifies that a Checkpoint correctly captures
execution state and workflow state.
"""

from app.runtime.state.checkpoint import Checkpoint
from app.runtime.state.execution_state import ExecutionState
from app.runtime.state.execution_status import ExecutionStatus
from app.runtime.state.workflow_state import WorkflowState


def test_checkpoint_recovery():

    print("\n==============================")
    print(" Checkpoint Recovery Test ")
    print("==============================\n")

    # ----------------------------------------
    # Create execution state
    # ----------------------------------------

    execution_state = ExecutionState(
        execution_id="execution-001",
    )

    execution_state.transition_to(
        ExecutionStatus.QUEUED
    )

    execution_state.transition_to(
        ExecutionStatus.RUNNING
    )

    # ----------------------------------------
    # Create workflow state
    # ----------------------------------------

    workflow_state = WorkflowState(
        workflow_id="book_ticket",
        total_steps=5,
    )

    workflow_state.complete_step()
    workflow_state.complete_step()

    # ----------------------------------------
    # Create checkpoint
    # ----------------------------------------

    checkpoint = Checkpoint(
        checkpoint_id="checkpoint-001",
        execution_state=execution_state,
        workflow_state=workflow_state,
    )

    print("Checkpoint created.\n")

    print(f"Checkpoint ID : {checkpoint.checkpoint_id}")
    print(f"Version       : {checkpoint.version}")
    print(f"Status        : {checkpoint.execution_state.status.name}")
    print(f"Workflow      : {checkpoint.workflow_state.workflow_id}")
    print(
        f"Completed     : "
        f"{checkpoint.workflow_state.completed_steps}/"
        f"{checkpoint.workflow_state.total_steps}"
    )

    # ----------------------------------------
    # Assertions
    # ----------------------------------------

    assert checkpoint.checkpoint_id == "checkpoint-001"

    assert (
        checkpoint.execution_state.status
        == ExecutionStatus.RUNNING
    )

    assert checkpoint.workflow_state.completed_steps == 2

    assert checkpoint.workflow_state.total_steps == 5

    assert checkpoint.version == 1

    print("\n✅ Checkpoint Recovery Test Passed!")


if __name__ == "__main__":
    test_checkpoint_recovery()
