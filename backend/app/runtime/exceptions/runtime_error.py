"""
Base exception hierarchy for the Agent Runtime.

All runtime-specific exceptions should inherit from AgentRuntimeError.
"""
from __future__ import annotations


class AgentRuntimeError(Exception):
    """
    Base exception for all Agent Runtime errors.

    Parameters
    ----------
    message:
        Human-readable description of the error.
    cause:
        Optional underlying exception.
    """

    def __init__(
        self,
        message: str = "An Agent Runtime error occurred.",
        *,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(message)
        self.cause = cause
