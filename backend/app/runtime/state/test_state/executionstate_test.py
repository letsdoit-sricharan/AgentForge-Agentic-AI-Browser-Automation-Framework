from app.runtime.state import ExecutionState ,Checkpoint
from app.runtime.state import WorkflowState 


execution = ExecutionState(execution_id="exec-001")

workflow = WorkflowState(
    workflow_id="wf-001",
    total_steps=10,
)

checkpoint = Checkpoint(
    checkpoint_id="cp-001",
    execution_state=execution,
    workflow_state=workflow,
)

assert checkpoint.execution_state is execution
assert checkpoint.workflow_state is workflow
assert checkpoint.version == 1