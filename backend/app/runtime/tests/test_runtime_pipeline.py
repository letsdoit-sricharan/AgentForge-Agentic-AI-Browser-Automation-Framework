"""
Runtime Pipeline Integration Test.

Verifies the complete execution flow:

ExecutionEngine
    ↓
ExecutionQueue
    ↓
WorkflowExecutor
    ↓
TaskExecutor
    ↓
BrowserExecutor
"""

import asyncio

from app.runtime.execution.execution_context import ExecutionContext
from app.runtime.execution.execution_metadata import ExecutionMetadata
from app.runtime.execution.execution_queue import ExecutionQueue
from app.runtime.execution.execution_request import ExecutionRequest
from app.runtime.execution.execution_engine import ExecutionEngine
from app.runtime.executors.browser_executor import BrowserExecutor
from app.runtime.executors.task_executor import TaskExecutor
from app.runtime.executors.workflow_executor import WorkflowExecutor
from app.runtime.memory.runtime_memory import RuntimeMemory
from app.runtime.state.execution_state import ExecutionState
from app.runtime.state.execution_status import ExecutionStatus
from app.runtime.state.workflow_state import WorkflowState
from app.runtime.strategies.navigation_strategy import NavigationStrategy
from app.runtime.strategies.recovery_strategy import RecoveryStrategy
from app.runtime.strategies.retry_strategy import RetryStrategy
from app.runtime.strategies.wait_strategy import WaitStrategy


# ---------------------------------------------------------------------
# Fake Browser Engine
# ---------------------------------------------------------------------


class FakeSession:
    async def close(self):
        print("Session closed.")


class FakeBrowser:
    async def new_session(self):
        print("Session created.")
        return FakeSession()


# ---------------------------------------------------------------------
# Sample Browser Tasks
# ---------------------------------------------------------------------


async def select_movie(context, session):
    print("Selecting movie...")
    context.memory.set("movie", "Coolie")
    return "movie selected"


async def select_theatre(context, session):
    movie = context.memory.get("movie")
    print(f"Selecting theatre for {movie}...")
    return "theatre selected"


# ---------------------------------------------------------------------
# Integration Test
# ---------------------------------------------------------------------


async def test_runtime_pipeline():

    print("\n==============================")
    print(" Agent Runtime Pipeline Test ")
    print("==============================\n")

    context = ExecutionContext(
        request=ExecutionRequest(
            plugin="bookmyshow",
            workflow="book_ticket",
        ),
        metadata=ExecutionMetadata(),
        execution_state=ExecutionState("exec-1"),
        workflow_state=WorkflowState(
            workflow_id="workflow-1",
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

    engine = ExecutionEngine(
        queue=ExecutionQueue(),
        workflow_executor=workflow_executor,
        retry_strategy=RetryStrategy(),
        wait_strategy=WaitStrategy(delay=0.1),
        recovery_strategy=RecoveryStrategy(),
        navigation_strategy=NavigationStrategy(),
    )

    result = await engine.execute(
        context=context,
        tasks=[
            select_movie,
            select_theatre,
        ],
    )

    # ---------------------------------------------------------
    # Assertions
    # ---------------------------------------------------------

    assert result.success

    assert (
        result.status
        == ExecutionStatus.COMPLETED
    )

    assert (
        context.execution_state.status
        == ExecutionStatus.COMPLETED
    )

    assert (
        context.workflow_state.completed_steps
        == 2
    )

    assert (
        context.memory.get("movie")
        == "Coolie"
    )

    print("\nRuntime finished successfully.")

    print(
        f"Execution ID : {context.execution_id}"
    )

    print(
        f"Workflow     : {context.workflow}"
    )

    print(
        f"Movie        : {context.memory.get('movie')}"
    )

    print("\n✅ Runtime pipeline test passed!")


if __name__ == "__main__":
    asyncio.run(test_runtime_pipeline())
