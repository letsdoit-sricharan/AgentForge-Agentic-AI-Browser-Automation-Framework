"""
Execution-related exceptions.
"""
from __future__ import annotations

from .runtime_error import AgentRuntimeError


class ExecutionError(AgentRuntimeError):
    """
    Raised when an execution fails unexpectedly.
    """

    def __init__(
        self,
        message: str = "Execution failed.",
        *,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(message, cause=cause)
