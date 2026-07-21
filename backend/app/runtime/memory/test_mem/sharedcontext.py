from app.runtime.memory.runtime_memory import RuntimeMemory
from app.runtime.memory.shared_context import SharedContext
from app.runtime.state.execution_state import ExecutionState
from app.runtime.state.workflow_state import WorkflowState


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
