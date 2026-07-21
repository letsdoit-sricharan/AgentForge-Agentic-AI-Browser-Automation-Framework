"""
Checkpoint-related exceptions.
"""

from .runtime_error import AgentRuntimeError


class CheckpointError(AgentRuntimeError):
    """
    Raised when checkpoint creation or restoration fails.
    """

    def __init__(
        self,
        message: str = "Checkpoint operation failed.",
        *,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(message, cause=cause)
