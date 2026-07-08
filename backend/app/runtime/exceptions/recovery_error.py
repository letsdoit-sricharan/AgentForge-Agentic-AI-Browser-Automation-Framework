"""
Recovery-related exceptions.
"""

from .runtime_error import AgentRuntimeError


class RecoveryError(AgentRuntimeError):
    """
    Raised when runtime recovery fails.
    """

    def __init__(
        self,
        message: str = "Recovery process failed.",
        *,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(message, cause=cause)