from app.runtime.state.execution_state import ExecutionState
from app.runtime.state.execution_status import ExecutionStatus
from app.runtime.exceptions.state_error import StateError

state = ExecutionState(execution_id="123")

state.transition_to(ExecutionStatus.QUEUED)
state.transition_to(ExecutionStatus.RUNNING)
state.transition_to(ExecutionStatus.COMPLETED)

try:
    state.transition_to(ExecutionStatus.RUNNING)
except StateError as e:
    print("Caught expected exception!")
    print(e)
