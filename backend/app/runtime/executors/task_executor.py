"""
Task executor.

Executes a single runtime task.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from app.runtime.execution.execution_context import ExecutionContext
from app.runtime.execution.execution_result import ExecutionResult
from app.runtime.executors.browser_executor import (
    BrowserExecutor,
    BrowserTask,
)
from app.runtime.state.execution_status import ExecutionStatus

Task = Callable[
    [ExecutionContext],
    Awaitable[Any],
]


class TaskExecutor:
    """
    Executes a single task.

    A task represents one unit of work within a workflow.
    """

    def __init__(
        self,
        browser_executor: BrowserExecutor,
    ) -> None:
        self._browser_executor = browser_executor

    async def execute(
        self,
        context: ExecutionContext,
        browser_task: BrowserTask,
    ) -> ExecutionResult:
        """
        Execute a single browser task.

        Args:
            context:
                Runtime execution context.

            browser_task:
                Browser task supplied by the plugin.

        Returns:
            ExecutionResult.
        """

        context.execution_state.status = ExecutionStatus.RUNNING

        try:
            output = await self._browser_executor.execute(
                context,
                browser_task,
            )

            context.execution_state.status = (
                ExecutionStatus.COMPLETED
            )

            return ExecutionResult(
                execution_id=context.execution_id,
                status=ExecutionStatus.COMPLETED,
                output={
                    "result": output,
                },
            )

        except Exception as exc:

            context.execution_state.status = (
                ExecutionStatus.FAILED
            )

            return ExecutionResult(
                execution_id=context.execution_id,
                status=ExecutionStatus.FAILED,
                message=str(exc),
                errors=[str(exc)],
            )
