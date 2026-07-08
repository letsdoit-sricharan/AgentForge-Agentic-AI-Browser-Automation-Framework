from app.runtime.state import (
    ExecutionState,
    ExecutionStatus,
)
from app.runtime.exceptions import StateError

state = ExecutionState(execution_id="123")

state.transition_to(ExecutionStatus.QUEUED)
state.transition_to(ExecutionStatus.RUNNING)
state.transition_to(ExecutionStatus.COMPLETED)

try:
    state.transition_to(ExecutionStatus.RUNNING)
except StateError as e:
    print("Caught expected exception!")
    print(e)