"""
Task Result

Represents the outcome of task execution.

Responsibilities:
    - Encapsulate execution outcome
    - Provide standardized result format
    - Track execution metadata

Does NOT:
    - Execute tasks
    - Contain business logic
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any


class TaskStatus(Enum):
    """
    Task execution status.
    """

    PENDING = auto()      # Task created, not yet started
    EXECUTING = auto()    # Task currently executing
    COMPLETED = auto()    # Task completed successfully
    FAILED = auto()       # Task failed
    CANCELLED = auto()    # Task cancelled
    TIMEOUT = auto()      # Task timed out


@dataclass
class TaskResult:
    """
    Result of task execution.

    Provides a standardized way to return task outcomes regardless
    of which plugin or workflow executed the task.
    """

    task_id: str
    task_type: str
    status: TaskStatus

    # Execution timing
    started_at: datetime | None = None
    completed_at: datetime | None = None

    # Output data
    output: dict[str, Any] = field(default_factory=dict)

    # Error information
    errors: list[str] = field(default_factory=list)
    error_details: dict[str, Any] = field(default_factory=dict)

    # Execution metadata
    plugin_name: str | None = None
    workflow_name: str | None = None

    # Additional metadata
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def success(self) -> bool:
        """Check if task completed successfully."""
        return self.status == TaskStatus.COMPLETED

    @property
    def duration(self) -> float | None:
        """Get execution duration in seconds."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "status": self.status.name,
            "success": self.success,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration": self.duration,
            "output": self.output,
            "errors": self.errors,
            "error_details": self.error_details,
            "plugin_name": self.plugin_name,
            "workflow_name": self.workflow_name,
            "metadata": self.metadata,
        }
