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

if TYPE_CHECKING:
    from app.plugins.interfaces import Plugin, PluginMetadata


class PluginRegistry:
    """
    Central registry for AgentForge plugins.
    """

    def __init__(self) -> None:
        self._plugins: dict[str, Plugin] = {}
        self._metadata: dict[str, PluginMetadata] = {}

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
