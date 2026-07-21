"""
Strategy-related exceptions.
"""

from .runtime_error import AgentRuntimeError


class StrategyError(AgentRuntimeError):
    """
    Raised when a runtime strategy fails.
    """

    def __init__(
        self,
        message: str = "Strategy execution failed.",
        *,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(message, cause=cause)
