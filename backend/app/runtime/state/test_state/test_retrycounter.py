from app.runtime.state import ExecutionState
from app.runtime.state import ExecutionStatus
state = ExecutionState(execution_id="123")

print(state.retry_count)

state.increment_retry()
state.increment_retry()

print(state.retry_count)

state = ExecutionState(execution_id="123")

state.set_error("Button not found")

print(state.last_error)

state = ExecutionState(execution_id="123")

print(state.created_at)
print(state.updated_at)

state.transition_to(ExecutionStatus.QUEUED)

print(state.updated_at)