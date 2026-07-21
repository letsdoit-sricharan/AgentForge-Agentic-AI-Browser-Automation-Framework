"""
Execution lifecycle states for the Agent Runtime.
"""

from enum import Enum


class ExecutionStatus(str, Enum):
    """
    Represents the lifecycle state of an execution.
    """

    CREATED = "created"
    QUEUED = "queued"
    RUNNING = "running"
    WAITING = "waiting"
    PAUSED = "paused"
    RETRYING = "retrying"
    RECOVERING = "recovering"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

    @property
    def is_terminal(self) -> bool:
        """
        Returns True if the status represents a terminal state.
        """
        return self in {
            ExecutionStatus.COMPLETED,
            ExecutionStatus.FAILED,
            ExecutionStatus.CANCELLED,
        }
