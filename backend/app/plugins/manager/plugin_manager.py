"""
Purpose:
    Orchestrates plugin lifecycle management across the framework.

Responsibilities:
    - Load and register plugins.
    - Initialize plugins with PluginContext.
    - Execute plugin workflows.
    - Shutdown plugins.
    - Track plugin states.
    - Provide plugin discovery and lookup.

Does NOT:
    - Import Playwright.
    - Manage browser lifecycle directly.
    - Contain website-specific logic.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.exceptions.plugin_errors import (
    PluginExecutionError,
    PluginInitializationError,
    PluginStateError,
)
from app.plugins.interfaces.plugin_context import PluginContext
from app.plugins.manager.plugin_loader import PluginLoader
from app.plugins.models.plugin_state import PluginState
from app.plugins.registry.plugin_registry import PluginRegistry

if TYPE_CHECKING:
    from app.plugins.interfaces.plugin import Plugin

logger = logging.getLogger(__name__)


class PluginManager:
    """
    Central manager for the AgentForge plugin system.
    Orchestrates plugin loading, registration, initialization, and execution.
    """

    def __init__(
        self,
        loader: PluginLoader | None = None,
        registry: PluginRegistry | None = None,
    ) -> None:
        """
        Initialize the plugin manager.

        Args:
            loader: Plugin loader instance (creates default if None)
            registry: Plugin registry instance (creates default if None)
        """
        self._loader = loader or PluginLoader()
        self._registry = registry or PluginRegistry()
        self._logger = logger

    def load_plugin(
        self,
        plugin_name: str,
    ) -> None:
        """
        Load and register a plugin by name.

        Args:
            plugin_name: Name of the plugin to load

        Raises:
            PluginLoadError: If plugin cannot be loaded
            PluginAlreadyRegisteredError: If plugin is already registered
        """
        # Load the plugin
        plugin = self._loader.load_plugin(plugin_name)

        # Register the plugin
        self._registry.register(plugin)

        # Update state
        state = self._registry.get_state(plugin_name)
        state.mark_loaded()

        self._logger.info(f"Plugin '{plugin_name}' loaded successfully")

    def load_all_plugins(self) -> dict[str, bool]:
        """
        Discover and load all available plugins.

        Returns:
            Dictionary mapping plugin names to load success status
        """
        plugin_names = self._loader.discover_plugins()
        results = {}

        for plugin_name in plugin_names:
            try:
                self.load_plugin(plugin_name)
                results[plugin_name] = True
            except Exception as e:
                self._logger.error(f"Failed to load plugin '{plugin_name}': {e}")
                results[plugin_name] = False

        return results

    def initialize_plugin(
        self,
        plugin_name: str,
        context: PluginContext,
    ) -> None:
        """
        Initialize a plugin with the provided context.

        Args:
            plugin_name: Name of the plugin to initialize
            context: PluginContext to pass to the plugin

        Raises:
            PluginNotFoundError: If plugin doesn't exist
            PluginStateError: If plugin is not in LOADED state
            PluginInitializationError: If initialization fails
        """
        # Get plugin and state
        plugin = self._registry.get(plugin_name)
        state = self._registry.get_state(plugin_name)

        # Validate state
        if not state.can_initialize():
            raise PluginStateError(
                plugin_name=plugin_name,
                current_state=state.status.value,
                operation="initialize",
            )

        try:
            # Mark as initializing
            state.mark_initializing()

            # Initialize the plugin
            plugin.initialize(context)

            # Mark as ready
            state.mark_ready()

            self._logger.info(f"Plugin '{plugin_name}' initialized successfully")

        except Exception as e:
            state.mark_error(e)
            raise PluginInitializationError(
                plugin_name=plugin_name,
                reason=str(e),
            ) from e

    async def execute_plugin(
        self,
        plugin_name: str,
        workflow_context: WorkflowContext,
    ) -> Any:
        """
        Execute a plugin workflow.

        Args:
            plugin_name: Name of the plugin to execute
            workflow_context: WorkflowContext for the execution

        Returns:
            Plugin execution result

        Raises:
            PluginNotFoundError: If plugin doesn't exist
            PluginStateError: If plugin is not initialized
            PluginExecutionError: If execution fails
        """
        # Get plugin and state
        plugin = self._registry.get(plugin_name)
        state = self._registry.get_state(plugin_name)

        # Validate state
        if not state.can_execute():
            raise PluginStateError(
                plugin_name=plugin_name,
                current_state=state.status.value,
                operation="execute",
            )

        try:
            # Mark as executing
            state.mark_executing()

            # Execute the plugin
            result = await plugin.execute(workflow_context)

            # Mark execution complete
            state.mark_execution_complete()

            self._logger.info(f"Plugin '{plugin_name}' executed successfully")

            return result

        except Exception as e:
            state.mark_error(e)
            raise PluginExecutionError(
                plugin_name=plugin_name,
                reason=str(e),
            ) from e

    def shutdown_plugin(
        self,
        plugin_name: str,
    ) -> None:
        """
        Shutdown a plugin.

        Args:
            plugin_name: Name of the plugin to shutdown

        Raises:
            PluginNotFoundError: If plugin doesn't exist
            PluginStateError: If plugin cannot be shut down
        """
        # Get plugin and state
        plugin = self._registry.get(plugin_name)
        state = self._registry.get_state(plugin_name)

        # Validate state
        if not state.can_shutdown():
            raise PluginStateError(
                plugin_name=plugin_name,
                current_state=state.status.value,
                operation="shutdown",
            )

        try:
            # Mark as shutting down
            state.mark_shutting_down()

            # Shutdown the plugin
            plugin.shutdown()

            # Mark as shutdown
            state.mark_shutdown()

            self._logger.info(f"Plugin '{plugin_name}' shut down successfully")

        except Exception as e:
            state.mark_error(e)
            self._logger.error(f"Error shutting down plugin '{plugin_name}': {e}")
            # Don't raise - best effort shutdown

    def shutdown_all_plugins(self) -> None:
        """
        Shutdown all registered plugins.
        """
        for plugin in self._registry.get_all():
            try:
                self.shutdown_plugin(plugin.metadata.name)
            except Exception as e:
                self._logger.error(
                    f"Error shutting down plugin '{plugin.metadata.name}': {e}"
                )

    def get_plugin(
        self,
        plugin_name: str,
    ) -> Plugin:
        """
        Get a plugin instance by name.

        Args:
            plugin_name: Name of the plugin

        Returns:
            Plugin instance

        Raises:
            PluginNotFoundError: If plugin doesn't exist
        """
        return self._registry.get(plugin_name)

    def get_plugin_state(
        self,
        plugin_name: str,
    ) -> PluginState:
        """
        Get the state of a plugin.

        Args:
            plugin_name: Name of the plugin

        Returns:
            Plugin state

        Raises:
            PluginNotFoundError: If plugin doesn't exist
        """
        return self._registry.get_state(plugin_name)

    def list_plugins(self) -> list[str]:
        """
        List all registered plugin names.

        Returns:
            List of plugin names
        """
        return [plugin.metadata.name for plugin in self._registry.get_all()]

    def find_plugins_by_capability(
        self,
        capability: str,
    ) -> list[Plugin]:
        """
        Find all plugins with a specific capability.

        Args:
            capability: Capability to search for

        Returns:
            List of plugins with the capability
        """
        plugin_names = self._registry.find_by_capability(capability)
        return [self._registry.get(name) for name in plugin_names]

    def get_all_plugin_states(self) -> dict[str, PluginState]:
        """
        Get all plugin states.

        Returns:
            Dictionary mapping plugin names to their states
        """
        return self._registry.get_all_states()

    @property
    def loader(self) -> PluginLoader:
        """Get the plugin loader."""
        return self._loader

    @property
    def registry(self) -> PluginRegistry:
        """Get the plugin registry."""
        return self._registry
