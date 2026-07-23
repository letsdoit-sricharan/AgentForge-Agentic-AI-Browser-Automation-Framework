"""
Task Registry

Central registry for task types and their supporting plugins.

Responsibilities:
    - Register task types with plugins
    - Look up which plugins support which tasks
    - Provide task discovery
    - Maintain task metadata

Does NOT:
    - Execute tasks
    - Load plugins
    - Know about workflows
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from app.runtime.tasks.exceptions import (
    TaskNotSupportedError,
    TaskRegistrationError,
)
from app.runtime.tasks.task_metadata import TaskMetadata

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class TaskRegistry:
    """
    Central registry mapping task types to supporting plugins.

    Enables:
    - Plugin-agnostic task execution
    - Task discovery
    - Capability-based task resolution
    """

    def __init__(self) -> None:
        """Initialize the task registry."""
        # Map: task_type → list of plugin names
        self._task_to_plugins: dict[str, list[str]] = {}

        # Map: task_type → TaskMetadata
        self._task_metadata: dict[str, TaskMetadata] = {}

        # Map: plugin_name → list of task types
        self._plugin_to_tasks: dict[str, list[str]] = {}

        self._logger = logger

    def register_task(
        self,
        task_type: str,
        plugin_name: str,
        metadata: TaskMetadata | None = None,
    ) -> None:
        """
        Register that a plugin supports a task type.

        Args:
            task_type: Task type identifier (e.g., "search_movie")
            plugin_name: Name of plugin that supports this task
            metadata: Optional task metadata

        Raises:
            TaskRegistrationError: If registration fails
        """
        try:
            # Add plugin to task mapping
            if task_type not in self._task_to_plugins:
                self._task_to_plugins[task_type] = []

            if plugin_name not in self._task_to_plugins[task_type]:
                self._task_to_plugins[task_type].append(plugin_name)

            # Add task to plugin mapping
            if plugin_name not in self._plugin_to_tasks:
                self._plugin_to_tasks[plugin_name] = []

            if task_type not in self._plugin_to_tasks[plugin_name]:
                self._plugin_to_tasks[plugin_name].append(task_type)

            # Store metadata if provided
            if metadata:
                self._task_metadata[task_type] = metadata

            self._logger.info(
                f"Registered task '{task_type}' with plugin '{plugin_name}'"
            )

        except Exception as e:
            raise TaskRegistrationError(
                task_type,
                f"Failed to register with plugin '{plugin_name}': {str(e)}",
            ) from e

    def unregister_task(
        self,
        task_type: str,
        plugin_name: str,
    ) -> None:
        """
        Unregister a task from a plugin.

        Args:
            task_type: Task type identifier
            plugin_name: Plugin name
        """
        # Remove from task→plugin mapping
        if task_type in self._task_to_plugins:
            if plugin_name in self._task_to_plugins[task_type]:
                self._task_to_plugins[task_type].remove(plugin_name)

            # Clean up empty lists
            if not self._task_to_plugins[task_type]:
                del self._task_to_plugins[task_type]
                # Also remove metadata
                if task_type in self._task_metadata:
                    del self._task_metadata[task_type]

        # Remove from plugin→task mapping
        if plugin_name in self._plugin_to_tasks:
            if task_type in self._plugin_to_tasks[plugin_name]:
                self._plugin_to_tasks[plugin_name].remove(task_type)

            # Clean up empty lists
            if not self._plugin_to_tasks[plugin_name]:
                del self._plugin_to_tasks[plugin_name]

    def get_supporting_plugins(
        self,
        task_type: str,
    ) -> list[str]:
        """
        Get list of plugins that support a task type.

        Args:
            task_type: Task type identifier

        Returns:
            List of plugin names

        Raises:
            TaskNotSupportedError: If no plugins support the task
        """
        plugins = self._task_to_plugins.get(task_type, [])

        if not plugins:
            raise TaskNotSupportedError(
                task_type,
                "No plugins registered for this task type",
            )

        return plugins.copy()

    def is_task_supported(
        self,
        task_type: str,
    ) -> bool:
        """
        Check if any plugin supports a task type.

        Args:
            task_type: Task type identifier

        Returns:
            True if at least one plugin supports the task
        """
        return task_type in self._task_to_plugins and len(
            self._task_to_plugins[task_type]
        ) > 0

    def get_plugin_tasks(
        self,
        plugin_name: str,
    ) -> list[str]:
        """
        Get list of tasks supported by a plugin.

        Args:
            plugin_name: Plugin name

        Returns:
            List of task types
        """
        return self._plugin_to_tasks.get(plugin_name, []).copy()

    def get_task_metadata(
        self,
        task_type: str,
    ) -> TaskMetadata | None:
        """
        Get metadata for a task type.

        Args:
            task_type: Task type identifier

        Returns:
            TaskMetadata if available, None otherwise
        """
        return self._task_metadata.get(task_type)

    def get_all_task_types(self) -> list[str]:
        """
        Get all registered task types.

        Returns:
            List of task type identifiers
        """
        return list(self._task_to_plugins.keys())

    def get_all_plugins(self) -> list[str]:
        """
        Get all plugins that have registered tasks.

        Returns:
            List of plugin names
        """
        return list(self._plugin_to_tasks.keys())

    def clear(self) -> None:
        """
        Clear all registrations.

        Used primarily for testing.
        """
        self._task_to_plugins.clear()
        self._task_metadata.clear()
        self._plugin_to_tasks.clear()
        self._logger.debug("Cleared task registry")

    def get_statistics(self) -> dict[str, int]:
        """
        Get registry statistics.

        Returns:
            Dictionary with registry statistics
        """
        return {
            "total_tasks": len(self._task_to_plugins),
            "total_plugins": len(self._plugin_to_tasks),
            "total_metadata_entries": len(self._task_metadata),
        }
