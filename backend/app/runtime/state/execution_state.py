"""
Execution state model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, UTC

from .execution_status import ExecutionStatus
from .state_machine import StateMachine


@dataclass()
class ExecutionState:
    """
    Represents the current execution state.
    """

    execution_id: str

    status: ExecutionStatus = ExecutionStatus.CREATED

    retry_count: int = 0

    current_task: str | None = None

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    started_at: datetime | None = None

    completed_at: datetime | None = None

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    last_error: str | None = None

    def transition_to(self, status: ExecutionStatus) -> None:
        """
        Transition to a new execution status.
        """

        StateMachine.validate_transition(
            self.status,
            status,
        )

        self.status = status
        self.updated_at = datetime.now(UTC)

        if status == ExecutionStatus.RUNNING and self.started_at is None:
            self.started_at = self.updated_at

        if status.is_terminal:
            self.completed_at = self.updated_at

    @property
    def is_terminal(self) -> bool:
        """
        Returns True if execution has completed.
        """
        return self.status.is_terminal

    def increment_retry(self) -> None:
        """
        Increment retry counter.
        """
        self.retry_count += 1

    def set_current_task(
        self,
        task_name: str | None,
    ) -> None:
        """
        Updates the currently executing task.
        """
        self.current_task = task_name
        self.updated_at = datetime.now(UTC)

    def set_error(
        self,
        message: str,
    ) -> None:
        """
        Stores the latest execution error.
        """
        self.last_error = message
        self.updated_at = datetime.now(UTC)
