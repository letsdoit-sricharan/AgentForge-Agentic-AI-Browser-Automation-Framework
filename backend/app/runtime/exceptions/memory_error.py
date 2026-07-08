"""
Runtime memory exceptions.
"""

from .runtime_error import AgentRuntimeError


class MemoryError(AgentRuntimeError):
    """
    Raised when runtime memory operations fail.
    """

    def __init__(
        self,
        message: str = "Runtime memory operation failed.",
        *,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(message, cause=cause)