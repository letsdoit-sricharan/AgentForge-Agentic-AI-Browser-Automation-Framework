"""
Purpose:
    Centralized registry for all loaded plugins.

Responsibilities:
    - Register and unregister plugins.
    - Track plugin instances and metadata.
    - Provide plugin lookup by name.
    - Validate plugin uniqueness.

Does NOT:
    - Load plugins from disk.
    - Initialize plugins.
    - Execute plugins.
    - Manage plugin lifecycle state.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.plugins.exceptions import (
    PluginAlreadyRegisteredError,
    PluginNotFoundError,
)
from app.plugins.models.plugin_state import PluginState, PluginStatus

if TYPE_CHECKING:
    from app.plugins.interfaces import Plugin, PluginMetadata


class PluginRegistry:
    """
    Central registry for AgentForge plugins.
    """

    def __init__(self) -> None:
        self._plugins: dict[str, Plugin] = {}
        self._metadata: dict[str, PluginMetadata] = {}
        self._states: dict[str, PluginState] = {}

    def register(
        self,
        plugin: Plugin,
    ) -> None:
        """
        Register a plugin instance.

        Args:
            plugin: Plugin instance to register.

        Raises:
            PluginAlreadyRegisteredError: If plugin name already exists.
        """
        metadata = plugin.metadata
        plugin_name = metadata.name

        if plugin_name in self._plugins:
            raise PluginAlreadyRegisteredError(plugin_name)

        self._plugins[plugin_name] = plugin
        self._metadata[plugin_name] = metadata
        self._states[plugin_name] = PluginState(
            plugin_name=plugin_name,
            status=PluginStatus.UNLOADED,
        )

    def unregister(
        self,
        plugin_name: str,
    ) -> None:
        """
        Unregister a plugin by name.

        Args:
            plugin_name: Name of the plugin to unregister.

        Raises:
            PluginNotFoundError: If plugin does not exist.
        """
        if plugin_name not in self._plugins:
            raise PluginNotFoundError(plugin_name)

        del self._plugins[plugin_name]
        del self._metadata[plugin_name]
        del self._states[plugin_name]

    def get(
        self,
        plugin_name: str,
    ) -> Plugin:
        """
        Retrieve a plugin by name.

        Args:
            plugin_name: Name of the plugin.

        Returns:
            Plugin instance.

        Raises:
            PluginNotFoundError: If plugin does not exist.
        """
        if plugin_name not in self._plugins:
            raise PluginNotFoundError(plugin_name)

        return self._plugins[plugin_name]

    def get_metadata(
        self,
        plugin_name: str,
    ) -> PluginMetadata:
        """
        Retrieve plugin metadata by name.

        Args:
            plugin_name: Name of the plugin.

        Returns:
            PluginMetadata instance.

        Raises:
            PluginNotFoundError: If plugin does not exist.
        """
        if plugin_name not in self._metadata:
            raise PluginNotFoundError(plugin_name)

        return self._metadata[plugin_name]

    def has_plugin(
        self,
        plugin_name: str,
    ) -> bool:
        """
        Check if a plugin is registered.

        Args:
            plugin_name: Name of the plugin.

        Returns:
            True if plugin exists, False otherwise.
        """
        return plugin_name in self._plugins

    def list_plugins(self) -> list[str]:
        """
        List all registered plugin names.

        Returns:
            List of plugin names.
        """
        return list(self._plugins.keys())

    def list_metadata(self) -> list[PluginMetadata]:
        """
        List all registered plugin metadata.

        Returns:
            List of PluginMetadata instances.
        """
        return list(self._metadata.values())

    def find_by_capability(
        self,
        capability: str,
    ) -> list[str]:
        """
        Find all plugins supporting a specific capability.

        Args:
            capability: Capability to search for.

        Returns:
            List of plugin names supporting the capability.
        """
        return [
            name
            for name, metadata in self._metadata.items()
            if capability in metadata.capabilities
        ]

    def clear(self) -> None:
        """
        Clear all registered plugins.

        Use with caution - typically only for testing.
        """
        self._plugins.clear()
        self._metadata.clear()

    def count(self) -> int:
        """
        Return the number of registered plugins.

        Returns:
            Number of registered plugins.
        """
        return len(self._plugins)

    def get_all(self) -> list[Plugin]:
        """
        Return all registered plugin instances.

        Returns:
            List of Plugin instances.
        """
        return list(self._plugins.values())

    def get_state(self, plugin_name: str) -> PluginState:
        """
        Return the runtime state object for a registered plugin.

        The registry tracks only that a plugin is registered (UNLOADED).
        Full lifecycle state (LOADING, READY, etc.) is managed by PluginManager.

        Args:
            plugin_name: Name of the plugin.

        Returns:
            PluginState for the plugin.

        Raises:
            PluginNotFoundError: If plugin is not registered.
        """
        if plugin_name not in self._states:
            raise PluginNotFoundError(plugin_name)

        return self._states[plugin_name]

    def get_plugins_by_status(self, status: PluginStatus) -> list[Plugin]:
        """
        Return all plugins matching a given status.

        Note: The registry only has visibility of UNLOADED status. For other
        statuses, use PluginManager which tracks full lifecycle state.

        Args:
            status: The PluginStatus to filter by.

        Returns:
            List of Plugin instances with the given status.
        """
        if status == PluginStatus.UNLOADED:
            return list(self._plugins.values())
        return []

    def get_all_states(self) -> dict[str, PluginState]:
        """
        Return all plugin states.

        Returns:
            Dictionary mapping plugin names to their states.
        """
        return dict(self._states)

