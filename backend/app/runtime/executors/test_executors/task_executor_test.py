import asyncio

from app.runtime.execution.execution_context import ExecutionContext
from app.runtime.execution.execution_metadata import ExecutionMetadata
from app.runtime.execution.execution_request import ExecutionRequest
from app.runtime.executors.browser_executor import BrowserExecutor
from app.runtime.executors.task_executor import TaskExecutor
from app.runtime.memory.runtime_memory import RuntimeMemory
from app.runtime.state.execution_state import ExecutionState
from app.runtime.state.execution_status import ExecutionStatus
from app.runtime.state.workflow_state import WorkflowState


class FakeSession:
    async def close(self):
        pass


class FakeBrowser:
    async def new_session(self):
        return FakeSession()


async def browser_task(context, session):
    print("Executing browser task...")
    return {"movie": "Coolie"}


async def test_task_executor():

    context = ExecutionContext(
        request=ExecutionRequest(
            plugin="bookmyshow",
            workflow="book_ticket",
        ),
        metadata=ExecutionMetadata(),
        execution_state=ExecutionState("exec-1"),
        workflow_state=WorkflowState(
            workflow_id="wf-1",
            total_steps=5,
        ),
        memory=RuntimeMemory(),
    )

    browser_executor = BrowserExecutor(
        FakeBrowser()
    )

    executor = TaskExecutor(
        browser_executor
    )

    result = await executor.execute(
        context,
        browser_task,
    )

    assert result.success
    assert result.status == ExecutionStatus.COMPLETED
    assert result.output["result"]["movie"] == "Coolie"

    print("✅ TaskExecutor test passed!")


if __name__ == "__main__":
    asyncio.run(test_task_executor())
