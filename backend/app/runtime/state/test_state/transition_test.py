from app.runtime.state import (
    ExecutionState,
    ExecutionStatus,
)

state = ExecutionState(execution_id="123")

print(state.status)

state.transition_to(ExecutionStatus.QUEUED)
print(state.status)

state.transition_to(ExecutionStatus.RUNNING)
print(state.status)

state.transition_to(ExecutionStatus.COMPLETED)
print(state.status)