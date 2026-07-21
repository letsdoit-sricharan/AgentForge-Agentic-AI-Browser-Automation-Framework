"""
State Transition Integration Test.

Verifies that ExecutionState correctly transitions
through the execution lifecycle.
"""

from app.runtime.state.execution_state import ExecutionState
from app.runtime.state.execution_status import ExecutionStatus


def print_status(state: ExecutionState) -> None:
    """Print the current execution status."""
    print(f"Current Status : {state.status.name}")


def test_state_transitions():

    print("\n==============================")
    print(" State Transition Test ")
    print("==============================\n")

    state = ExecutionState(
        execution_id="execution-001"
    )

    # -------------------------------------------------
    # Initial State
    # -------------------------------------------------

    assert state.status == ExecutionStatus.CREATED
    print_status(state)

    # -------------------------------------------------
    # CREATED -> QUEUED
    # -------------------------------------------------

    state.transition_to(ExecutionStatus.QUEUED)

    assert state.status == ExecutionStatus.QUEUED
    print_status(state)

    # -------------------------------------------------
    # QUEUED -> RUNNING
    # -------------------------------------------------

    state.transition_to(ExecutionStatus.RUNNING)

    assert state.status == ExecutionStatus.RUNNING
    print_status(state)

    # -------------------------------------------------
    # RUNNING -> COMPLETED
    # -------------------------------------------------

    state.transition_to(ExecutionStatus.COMPLETED)

    assert state.status == ExecutionStatus.COMPLETED
    print_status(state)

    print("\n✅ Successful execution lifecycle verified!")

    # -------------------------------------------------
    # Failure Scenario
    # -------------------------------------------------

    print("\nTesting failure path...\n")

    failed_state = ExecutionState(
        execution_id="execution-002"
    )

    failed_state.transition_to(ExecutionStatus.QUEUED)
    failed_state.transition_to(ExecutionStatus.RUNNING)
    failed_state.transition_to(ExecutionStatus.FAILED)

    assert failed_state.status == ExecutionStatus.FAILED

    print_status(failed_state)

    print("\n✅ Failure lifecycle verified!")

    print("\n🎉 State Transition Test Passed!")


if __name__ == "__main__":
    test_state_transitions()
