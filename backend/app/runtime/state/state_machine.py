"""
Defines valid execution state transitions.
"""

from __future__ import annotations

from app.runtime.exceptions.state_error import StateError

from .execution_status import ExecutionStatus


class StateMachine:
    """
    Validates execution state transitions.
    """

    _TRANSITIONS = {
        ExecutionStatus.CREATED: {
            ExecutionStatus.QUEUED,
            ExecutionStatus.CANCELLED,
        },
        ExecutionStatus.QUEUED: {
            ExecutionStatus.RUNNING,
            ExecutionStatus.CANCELLED,
        },
        ExecutionStatus.RUNNING: {
            ExecutionStatus.WAITING,
            ExecutionStatus.PAUSED,
            ExecutionStatus.RETRYING,
            ExecutionStatus.RECOVERING,
            ExecutionStatus.COMPLETED,
            ExecutionStatus.FAILED,
            ExecutionStatus.CANCELLED,
        },
        ExecutionStatus.WAITING: {
            ExecutionStatus.RUNNING,
            ExecutionStatus.CANCELLED,
            ExecutionStatus.FAILED,
        },
        ExecutionStatus.PAUSED: {
            ExecutionStatus.RUNNING,
            ExecutionStatus.CANCELLED,
        },
        ExecutionStatus.RETRYING: {
            ExecutionStatus.RUNNING,
            ExecutionStatus.FAILED,
            ExecutionStatus.CANCELLED,
        },
        ExecutionStatus.RECOVERING: {
            ExecutionStatus.RUNNING,
            ExecutionStatus.FAILED,
            ExecutionStatus.CANCELLED,
        },
        ExecutionStatus.COMPLETED: set(),
        ExecutionStatus.FAILED: set(),
        ExecutionStatus.CANCELLED: set(),
    }

    @classmethod
    def can_transition(
        cls,
        current: ExecutionStatus,
        target: ExecutionStatus,
    ) -> bool:
        """
        Returns True if the transition is valid.
        """
        return target in cls._TRANSITIONS[current]

    @classmethod
    def validate_transition(
        cls,
        current: ExecutionStatus,
        target: ExecutionStatus,
    ) -> None:
        """
        Raises StateError if the transition is invalid.
        """
        if not cls.can_transition(current, target):
            raise StateError(
                f"Invalid execution state transition: "
                f"{current.value} -> {target.value}"
            )