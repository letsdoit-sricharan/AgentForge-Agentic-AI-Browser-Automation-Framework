"""
Recovery strategy.

Provides recovery behavior for failed runtime executions.

Responsibilities:
    - Reset execution state.
    - Optionally clear runtime memory.
    - Restore workflow state.

This strategy prepares an execution for another attempt.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.runtime.execution.execution_context import ExecutionContext
from app.runtime.state.execution_status import ExecutionStatus


@dataclass()
class RecoveryStrategy:
    """
    Generic recovery strategy.
    """

    clear_memory: bool = False

    reset_workflow: bool = False

    def recover(
        self,
        context: ExecutionContext,
    ) -> None:
        """
        Recover an execution context.

        Args:
            context:
                Execution context to recover.
        """

        # Reset execution status
        context.execution_state.status = ExecutionStatus.CREATED

        # Reset retry counter
        context.execution_state.retry_count = 0

        # Optionally clear runtime memory
        if self.clear_memory:
            context.memory.clear()

        # Optionally reset workflow progress
        if self.reset_workflow:
            context.workflow_state.current_step = None
            context.workflow_state.completed_steps = 0