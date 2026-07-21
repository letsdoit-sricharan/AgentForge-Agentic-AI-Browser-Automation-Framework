from app.runtime.state.execution_status import ExecutionStatus

print(ExecutionStatus.CREATED)
print(ExecutionStatus.RUNNING)

print(ExecutionStatus.COMPLETED.is_terminal)
print(ExecutionStatus.RUNNING.is_terminal)
