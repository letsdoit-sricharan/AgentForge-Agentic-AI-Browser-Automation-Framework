"""
Tests for BrowserExecutor.
"""

import asyncio

from app.runtime.execution.execution_context import ExecutionContext
from app.runtime.execution.execution_metadata import ExecutionMetadata
from app.runtime.execution.execution_request import ExecutionRequest
from app.runtime.executors.browser_executor import BrowserExecutor
from app.runtime.memory.runtime_memory import RuntimeMemory
from app.runtime.state.execution_state import ExecutionState
from app.runtime.state.workflow_state import WorkflowState


class FakeSession:
    async def close(self):
        print("Session closed.")


class FakeBrowser:
    async def new_session(self):
        print("Session created.")
        return FakeSession()


async def browser_task(context, session):
    print(f"Running workflow: {context.workflow}")
    return "SUCCESS"


async def test_browser_executor():
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

    executor = BrowserExecutor(FakeBrowser())

    result = await executor.execute(
        context,
        browser_task,
    )

    assert result == "SUCCESS"

    print("✅ BrowserExecutor test passed!")


if __name__ == "__main__":
    asyncio.run(test_browser_executor())
