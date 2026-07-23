"""
Task Factory

Factory for constructing tasks from structured data.

Responsibilities:
    - Create task instances from dictionaries
    - Validate task structure
    - Support multiple input formats
    - Bridge between AI planner and task system

Does NOT:
    - Execute tasks
    - Know about plugins
    - Contain business logic
"""

from __future__ import annotations

import logging
from typing import Any, Type

from app.runtime.tasks.exceptions import TaskValidationError
from app.runtime.tasks.task import Task

logger = logging.getLogger(__name__)


class TaskFactory:
    """
    Factory for creating Task instances from structured data.

    Used by:
    - AI Planner to convert plans to tasks
    - API layer to parse task requests
    - Task deserialization
    """

    def __init__(self) -> None:
        """Initialize the task factory."""
        # Registry of task type → Task class
        self._task_classes: dict[str, Type[Task]] = {}
        self._logger = logger

    def register_task_class(
        self,
        task_type: str,
        task_class: Type[Task],
    ) -> None:
        """
        Register a Task class for a task type.

        Args:
            task_type: Task type identifier
            task_class: Task class to instantiate
        """
        self._task_classes[task_type] = task_class
        self._logger.debug(f"Registered task class for type '{task_type}'")

    def create_task(
        self,
        task_type: str,
        **kwargs: Any,
    ) -> Task:
        """
        Create a task instance.

        Args:
            task_type: Task type identifier
            **kwargs: Task-specific parameters

        Returns:
            Task instance

        Raises:
            TaskValidationError: If task creation fails

        Example:
            >>> factory.create_task(
            ...     "search_movie",
            ...     movie="Inception",
            ...     city="Mumbai",
            ... )
            SearchMovieTask(movie="Inception", city="Mumbai")
        """
        if task_type not in self._task_classes:
            raise TaskValidationError(
                task_type,
                [f"Unknown task type: {task_type}"],
            )

        task_class = self._task_classes[task_type]

        try:
            task = task_class(**kwargs)

            # Validate the created task
            is_valid, errors = task.validate()
            if not is_valid:
                raise TaskValidationError(task_type, errors)

            self._logger.debug(f"Created task: {task}")
            return task

        except TaskValidationError:
            raise
        except Exception as e:
            raise TaskValidationError(
                task_type,
                [f"Failed to create task: {str(e)}"],
            ) from e

    def create_from_dict(
        self,
        data: dict[str, Any],
    ) -> Task:
        """
        Create a task from dictionary representation.

        Args:
            data: Dictionary containing task data

        Returns:
            Task instance

        Raises:
            TaskValidationError: If task creation fails

        Example:
            >>> factory.create_from_dict({
            ...     "task_type": "search_movie",
            ...     "movie": "Inception",
            ...     "city": "Mumbai",
            ... })
            SearchMovieTask(movie="Inception", city="Mumbai")
        """
        if "task_type" not in data:
            raise TaskValidationError(
                "unknown",
                ["Missing required field: task_type"],
            )

        task_type = data.pop("task_type")
        return self.create_task(task_type, **data)

    def is_task_type_registered(
        self,
        task_type: str,
    ) -> bool:
        """
        Check if a task type is registered.

        Args:
            task_type: Task type identifier

        Returns:
            True if task type is registered
        """
        return task_type in self._task_classes

    def get_registered_task_types(self) -> list[str]:
        """
        Get all registered task types.

        Returns:
            List of task type identifiers
        """
        return list(self._task_classes.keys())

    def clear(self) -> None:
        """
        Clear all registered task classes.

        Used primarily for testing.
        """
        self._task_classes.clear()
        self._logger.debug("Cleared task factory")
