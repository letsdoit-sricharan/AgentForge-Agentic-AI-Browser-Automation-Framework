"""
Purpose:
    Manages the lifecycle of registered plugins.

Responsibilities:
    - Initialize plugins.
    - Execute plugins.
    - Shutdown plugins.
    - Update ManagedPlugin runtime information.

Does NOT:
    - Discover plugins.
    - Register plugins.
    - Import plugin modules.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.plugins.exceptions import PluginExecutionError
from app.plugins.interfaces import PluginContext
from app.plugins.models import ManagedPlugin, PluginState
from app.plugins.registry import PluginRegistry


class PluginManager:
    """
    Manages the lifecycle of registered plugins.
    """

    def __init__(self, registry: PluginRegistry) -> None:
        self._registry = registry

    def initialize(
        self,
        plugin_name: str,
        context: PluginContext,
    ) -> None:
        """
        Initialize a plugin.
        """

        managed = self._registry.get(plugin_name)

        managed.plugin.initialize(context)

        managed.context = context
        managed.state = PluginState.INITIALIZED
        managed.initialized_at = datetime.utcnow()

    def execute(
        self,
        plugin_name: str,
        task: Any,
    ) -> Any:
        """
        Execute a plugin task.
        """

        managed = self._registry.get(plugin_name)

        managed.state = PluginState.RUNNING
        managed.execution_count += 1
        managed.last_execution_at = datetime.utcnow()

        try:

            return managed.plugin.execute(task)

        except Exception as exc:

            managed.state = PluginState.FAILED
            managed.last_error = exc

            raise PluginExecutionError(
                f"Plugin '{plugin_name}' execution failed."
            ) from exc

    def shutdown(
        self,
        plugin_name: str,
    ) -> None:
        """
        Shutdown a plugin.
        """

        managed = self._registry.get(plugin_name)

        managed.plugin.shutdown()

        managed.state = PluginState.STOPPED

    def get_state(
        self,
        plugin_name: str,
    ) -> PluginState:
        """
        Return the current plugin state.
        """

        return self._registry.get(plugin_name).state

    def get_managed_plugin(
        self,
        plugin_name: str,
    ) -> ManagedPlugin:
        """
        Return the ManagedPlugin instance.
        """

        return self._registry.get(plugin_name)

    def is_initialized(
        self,
        plugin_name: str,
    ) -> bool:
        return (
            self.get_state(plugin_name)
            == PluginState.INITIALIZED
        )

    def is_running(
        self,
        plugin_name: str,
    ) -> bool:
        return (
            self.get_state(plugin_name)
            == PluginState.RUNNING
        )