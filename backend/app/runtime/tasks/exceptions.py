"""
Task Exceptions

Exception hierarchy for the task abstraction layer.

Responsibilities:
    - Define task-specific exceptions
    - Provide context for task failures
    - Separate task errors from plugin/runtime errors

Does NOT:
    - Handle exceptions
    - Contain business logic
"""

from __future__ import annotations


class TaskError(Exception):
    """
    Base exception for all task-related errors.
    """

    pass


class TaskValidationError(TaskError):
    """
    Raised when task validation fails.
    """

    def __init__(self, task_type: str, errors: list[str]) -> None:
        self.task_type = task_type
        self.errors = errors
        error_list = "\n  - ".join(errors)
        super().__init__(f"Task validation failed for '{task_type}':\n  - {error_list}")


class TaskNotSupportedError(TaskError):
    """
    Raised when no plugin supports a requested task.
    """

    def __init__(self, task_type: str, reason: str | None = None) -> None:
        self.task_type = task_type
        self.reason = reason
        msg = f"No plugin supports task type '{task_type}'"
        if reason:
            msg += f": {reason}"
        super().__init__(msg)


class TaskExecutionError(TaskError):
    """
    Raised when task execution fails.
    """

    def __init__(self, task_type: str, reason: str) -> None:
        self.task_type = task_type
        self.reason = reason
        super().__init__(f"Task execution failed for '{task_type}': {reason}")


class TaskRegistrationError(TaskError):
    """
    Raised when task registration fails.
    """

    def __init__(self, task_type: str, reason: str) -> None:
        self.task_type = task_type
        self.reason = reason
        super().__init__(f"Task registration failed for '{task_type}': {reason}")


class TaskResolutionError(TaskError):
    """
    Raised when task resolution fails.
    """

    def __init__(self, task_type: str, reason: str) -> None:
        self.task_type = task_type
        self.reason = reason
        super().__init__(f"Task resolution failed for '{task_type}': {reason}")
