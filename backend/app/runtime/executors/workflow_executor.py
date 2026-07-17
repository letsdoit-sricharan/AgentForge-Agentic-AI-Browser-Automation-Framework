"""
Workflow executor.

Coordinates the execution of workflow tasks.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from app.runtime.execution.execution_context import ExecutionContext
from app.runtime.execution.execution_result import ExecutionResult
from app.runtime.executors.task_executor import (
    BrowserTask,
    TaskExecutor,
)
from app.runtime.state.execution_status import ExecutionStatus


class WorkflowExecutor:
    """
    Executes a workflow consisting of multiple tasks.
    """

    def __init__(
        self,
        task_executor: TaskExecutor,
    ) -> None:
        self._task_executor = task_executor

    async def execute(
        self,
        context: ExecutionContext,
        tasks: list[BrowserTask],
    ) -> ExecutionResult:
        """
        Execute all workflow tasks sequentially.

        Args:
            context:
                Runtime execution context.

            tasks:
                Ordered list of workflow tasks.

        Returns:
            ExecutionResult.
        """

        context.execution_state.status = (
            ExecutionStatus.RUNNING
        )

        total = len(tasks)
        context.workflow_state.total_steps = total

        for index, task in enumerate(tasks, start=1):

            context.workflow_state.current_step = (
                f"step-{index}"
            )

            result = await self._task_executor.execute(
                context,
                task,
            )

            if not result.success:

                context.execution_state.status = (
                    ExecutionStatus.FAILED
                )

                return result

            context.workflow_state.completed_steps = (
                index
            )

        context.execution_state.status = (
            ExecutionStatus.COMPLETED
        )

        return ExecutionResult(
            execution_id=context.execution_id,
            status=ExecutionStatus.COMPLETED,
            output={
                "completed_steps": total,
            },
        )