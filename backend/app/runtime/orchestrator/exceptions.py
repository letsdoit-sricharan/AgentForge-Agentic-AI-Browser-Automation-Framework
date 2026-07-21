"""
Orchestrator Exceptions

Exception hierarchy for the execution orchestrator.

Responsibilities:
    - Define orchestration-specific exceptions
    - Provide context for orchestration failures
    - Separate orchestration errors from plugin/runtime errors

Does NOT:
    - Handle exceptions
    - Contain business logic
"""


class OrchestrationError(Exception):
    """
    Base exception for all orchestration errors.
    """

    pass


class PluginResolutionError(OrchestrationError):
    """
    Raised when plugin resolution fails.
    """

    def __init__(self, plugin_name: str, reason: str) -> None:
        self.plugin_name = plugin_name
        self.reason = reason
        super().__init__(f"Failed to resolve plugin '{plugin_name}': {reason}")


class WorkflowResolutionError(OrchestrationError):
    """
    Raised when workflow resolution fails.
    """

    def __init__(self, workflow_name: str, plugin_name: str, reason: str) -> None:
        self.workflow_name = workflow_name
        self.plugin_name = plugin_name
        self.reason = reason
        super().__init__(
            f"Failed to resolve workflow '{workflow_name}' "
            f"in plugin '{plugin_name}': {reason}"
        )


class ExecutionPreparationError(OrchestrationError):
    """
    Raised when execution preparation fails.
    """

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(f"Execution preparation failed: {reason}")


class WorkflowContextCreationError(OrchestrationError):
    """
    Raised when WorkflowContext creation fails.
    """

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(f"Failed to create WorkflowContext: {reason}")


class OrchestrationPipelineError(OrchestrationError):
    """
    Raised when the orchestration pipeline encounters an error.
    """

    def __init__(self, stage: str, reason: str) -> None:
        self.stage = stage
        self.reason = reason
        super().__init__(f"Pipeline failed at stage '{stage}': {reason}")
