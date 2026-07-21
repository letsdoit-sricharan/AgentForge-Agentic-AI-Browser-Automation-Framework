"""
Task Abstraction Layer

Provides a generic task execution system that sits between AI planners
and plugin workflows.

Architecture:
    User Goal → AI Planner → Tasks → Task Executor → Plugin Workflows

Key Principles:
    - Tasks represent business objectives, not implementations
    - Tasks are plugin-agnostic
    - Tasks are browser-agnostic
    - Tasks describe WHAT, not HOW
"""

from app.runtime.tasks.exceptions import (
    TaskError,
    TaskExecutionError,
    TaskNotSupportedError,
    TaskRegistrationError,
    TaskValidationError,
)
from app.runtime.tasks.task import Task
from app.runtime.tasks.task_capability import TaskCapability
from app.runtime.tasks.task_context import TaskContext
from app.runtime.tasks.task_executor import TaskExecutor
from app.runtime.tasks.task_factory import TaskFactory
from app.runtime.tasks.task_metadata import TaskMetadata
from app.runtime.tasks.task_registry import TaskRegistry
from app.runtime.tasks.task_result import TaskResult, TaskStatus

__all__ = [
    # Core
    "Task",
    "TaskContext",
    "TaskResult",
    "TaskStatus",
    # Metadata
    "TaskMetadata",
    "TaskCapability",
    # Execution
    "TaskExecutor",
    "TaskFactory",
    "TaskRegistry",
    # Exceptions
    "TaskError",
    "TaskExecutionError",
    "TaskNotSupportedError",
    "TaskRegistrationError",
    "TaskValidationError",
]
