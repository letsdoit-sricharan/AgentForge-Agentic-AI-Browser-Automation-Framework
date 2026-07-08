"""
Workflow-related exceptions.
"""

from .runtime_error import AgentRuntimeError


class WorkflowError(AgentRuntimeError):
    """
    Raised when workflow execution fails.
    """

    def __init__(
        self,
        message: str = "Workflow execution failed.",
        *,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(message, cause=cause)