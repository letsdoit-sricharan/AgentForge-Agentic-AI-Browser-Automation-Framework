"""
Execution state exceptions.
"""
from __future__ import annotations

from .runtime_error import AgentRuntimeError


class StateError(AgentRuntimeError):
    """
    Raised when an invalid execution state transition occurs.
    """

    def __init__(
        self,
        message: str = "Invalid execution state.",
        *,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(message, cause=cause)
