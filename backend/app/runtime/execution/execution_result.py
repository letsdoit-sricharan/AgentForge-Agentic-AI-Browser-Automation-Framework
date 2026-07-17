"""
Execution result model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from app.runtime.state.execution_status import ExecutionStatus


@dataclass(slots=True)
class ExecutionResult:
    """
    Final result produced by the runtime.

    Represents the outcome of an execution.
    """

    execution_id: str

    status: ExecutionStatus

    message: str | None = None

    output: dict[str, Any] = field(default_factory=dict)

    artifacts: dict[str, Any] = field(default_factory=dict)

    errors: list[str] = field(default_factory=list)

    started_at: datetime | None = None

    completed_at: datetime | None = None

    @property
    def success(self) -> bool:
        """
        Returns True if execution completed successfully.
        """
        return self.status == ExecutionStatus.COMPLETED

    @property
    def duration(self) -> float | None:
        """
        Returns execution duration in seconds.

        Returns:
            None if timestamps are unavailable.
        """
        if self.started_at is None or self.completed_at is None:
            return None

        return (
            self.completed_at - self.started_at
        ).total_seconds()