from app.runtime.state.workflow_state import WorkflowState
workflow = WorkflowState(
    workflow_id="wf-001",
    total_steps=5,
)

assert workflow.progress == 0

workflow.complete_step()

assert workflow.completed_steps == 1
assert workflow.progress == 20.0

workflow.set_current_step("Select Seats")
assert workflow.current_step == "Select Seats"

workflow.set_failed_step("Payment")
assert workflow.failed_step == "Payment"