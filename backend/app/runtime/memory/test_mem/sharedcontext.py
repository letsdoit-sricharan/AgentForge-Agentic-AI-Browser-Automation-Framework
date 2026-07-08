from app.runtime.memory import RuntimeMemory, SharedContext
from app.runtime.state import ExecutionState, WorkflowState


def test_shared_context():
    context = SharedContext(
        execution_state=ExecutionState("exec-1"),
        workflow_state=WorkflowState(
            workflow_id="wf-1",
            total_steps=5,
        ),
        memory=RuntimeMemory(),
    )

    assert context.execution_state.execution_id == "exec-1"
    assert context.workflow_state.workflow_id == "wf-1"
    assert context.memory.size == 0