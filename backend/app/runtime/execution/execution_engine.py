"""
Execution engine.

Coordinates runtime execution.

The execution engine orchestrates the execution lifecycle by
delegating work to the runtime components. It intentionally
contains very little business logic.
"""


from __future__ import annotations

from typing import TYPE_CHECKING

from app.runtime.execution.execution_context import ExecutionContext
from app.runtime.execution.execution_queue import ExecutionQueue
from app.runtime.execution.execution_result import ExecutionResult
from app.runtime.strategies.navigation_strategy import NavigationDecision

if TYPE_CHECKING:
    from app.runtime.executors.workflow_executor import WorkflowExecutor
    from app.runtime.strategies.navigation_strategy import NavigationStrategy
    from app.runtime.strategies.recovery_strategy import RecoveryStrategy
    from app.runtime.strategies.retry_strategy import RetryStrategy
    from app.runtime.strategies.wait_strategy import WaitStrategy


class ExecutionEngine:
    """
    Coordinates runtime execution.
    """

    def __init__(
        self,
        queue: ExecutionQueue,
        workflow_executor: WorkflowExecutor,
        retry_strategy: RetryStrategy,
        wait_strategy: WaitStrategy,
        recovery_strategy: RecoveryStrategy,
        navigation_strategy: NavigationStrategy,
    ) -> None:

        self._queue = queue

        self._workflow_executor = workflow_executor

        self._retry_strategy = retry_strategy

        self._wait_strategy = wait_strategy

        self._recovery_strategy = recovery_strategy

        self._navigation_strategy = navigation_strategy

    async def execute(
        self,
        context: ExecutionContext,
        tasks: list,
    ) -> ExecutionResult:
        """
        Execute a workflow.

        Args:
            context:
                Execution context.

            tasks:
                Workflow tasks.

        Returns:
            ExecutionResult.
        """

        self._queue.enqueue(context)

        queued_context = self._queue.dequeue()

        if queued_context is None:
            raise RuntimeError(
                "Execution queue unexpectedly empty."
            )

        while True:

            result = await self._workflow_executor.execute(
                queued_context,
                tasks,
            )

            if result.success:
                return result

            if not self._retry_strategy.should_retry():
                return result

            self._retry_strategy.record_retry()

            await self._wait_strategy.wait()

            self._recovery_strategy.recover(
                queued_context
            )

            decision = self._navigation_strategy.on_failure(
                retry_available=True,
                checkpoint_available=False,
            )

            if decision == NavigationDecision.ABORT:
                return result
