from app.runtime.state.execution_state import ExecutionState
from app.runtime.state.execution_status import ExecutionStatus

state = ExecutionState(execution_id="123")

print(state.status)

state.transition_to(ExecutionStatus.QUEUED)
print(state.status)

state.transition_to(ExecutionStatus.RUNNING)
print(state.status)

state.transition_to(ExecutionStatus.COMPLETED)
print(state.status)
