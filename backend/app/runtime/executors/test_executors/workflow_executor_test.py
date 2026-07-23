import asyncio

from app.runtime.execution.execution_context import ExecutionContext
from app.runtime.execution.execution_metadata import ExecutionMetadata
from app.runtime.execution.execution_request import ExecutionRequest
from app.runtime.executors.browser_executor import BrowserExecutor
from app.runtime.executors.task_executor import TaskExecutor
from app.runtime.executors.workflow_executor import WorkflowExecutor
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


async def task_one(context, session):
    print("Executing Task 1")
    return "task1"


async def task_two(context, session):
    print("Executing Task 2")
    return "task2"


async def test_workflow_executor():

    context = ExecutionContext(
        request=ExecutionRequest(
            plugin="bookmyshow",
            workflow="book_ticket",
        ),
        metadata=ExecutionMetadata(),
        execution_state=ExecutionState("exec-1"),
        workflow_state=WorkflowState(
            workflow_id="wf-1",
            total_steps=0,
        ),
        memory=RuntimeMemory(),
    )

    browser_executor = BrowserExecutor(
        FakeBrowser()
    )

    task_executor = TaskExecutor(
        browser_executor
    )

    workflow_executor = WorkflowExecutor(
        task_executor
    )

    result = await workflow_executor.execute(
        context,
        [
            task_one,
            task_two,
        ],
    )

    assert result.success

    assert (
        result.status
        == ExecutionStatus.COMPLETED
    )

    assert (
        context.workflow_state.completed_steps
        == 2
    )

    print("✅ WorkflowExecutor test passed!")


if __name__ == "__main__":
    asyncio.run(test_workflow_executor())
