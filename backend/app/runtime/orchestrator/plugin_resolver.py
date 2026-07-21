"""
Plugin Resolver

Determines which plugin should satisfy an execution request.

Responsibilities:
    - Query the Plugin Registry for plugins
    - Validate plugin availability
    - Validate plugin capabilities
    - Return plugin resolution result

Does NOT:
    - Initialize plugins
    - Execute plugins
    - Know about specific plugins (BookMyShow, etc.)
    - Manage browser lifecycle
    - Import Playwright
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from app.runtime.orchestrator.exceptions import PluginResolutionError
from app.runtime.orchestrator.models import PluginResolution

if TYPE_CHECKING:
    from app.plugins.registry import PluginRegistry

logger = logging.getLogger(__name__)


class PluginResolver:
    """
    Resolves which plugin should handle an execution request.
    """

    def __init__(
        self,
        registry: PluginRegistry,
    ) -> None:
        """
        Initialize the plugin resolver.

        Args:
            registry: Plugin registry to query
        """
        self._registry = registry
        self._logger = logger

    def resolve(
        self,
        plugin_name: str,
        required_capabilities: list[str] | None = None,
    ) -> PluginResolution:
        """
        Resolve a plugin by name.

        Args:
            plugin_name: Name of the plugin to resolve
            required_capabilities: Optional list of required capabilities

        Returns:
            PluginResolution with plugin instance or error

        Raises:
            PluginResolutionError: If resolution fails critically
        """
        self._logger.debug(f"Resolving plugin: {plugin_name}")

        # Check if plugin exists
        if not self._registry.has_plugin(plugin_name):
            error_msg = f"Plugin '{plugin_name}' not found in registry"
            self._logger.error(error_msg)
            return PluginResolution(
                plugin_name=plugin_name,
                found=False,
                error=error_msg,
            )

        try:
            # Get the plugin
            plugin = self._registry.get(plugin_name)

            # Validate capabilities if required
            if required_capabilities:
                missing_capabilities = self._validate_capabilities(
                    plugin, required_capabilities
                )
                if missing_capabilities:
                    error_msg = (
                        f"Plugin '{plugin_name}' missing required capabilities: "
                        f"{', '.join(missing_capabilities)}"
                    )
                    self._logger.warning(error_msg)
                    return PluginResolution(
                        plugin_name=plugin_name,
                        found=True,
                        plugin=plugin,
                        error=error_msg,
                        capabilities=plugin.metadata.capabilities,
                    )

            # Successfully resolved
            self._logger.info(f"Successfully resolved plugin: {plugin_name}")
            return PluginResolution(
                plugin_name=plugin_name,
                found=True,
                plugin=plugin,
                capabilities=plugin.metadata.capabilities,
            )

        except Exception as e:
            error_msg = f"Error resolving plugin '{plugin_name}': {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise PluginResolutionError(plugin_name, str(e)) from e

    def resolve_by_capability(
        self,
        capability: str,
    ) -> list[PluginResolution]:
        """
        Find all plugins with a specific capability.

        Args:
            capability: Capability to search for

        Returns:
            List of PluginResolution objects
        """
        self._logger.debug(f"Resolving plugins by capability: {capability}")

        plugins = self._registry.find_by_capability(capability)

        if not plugins:
            self._logger.warning(f"No plugins found with capability: {capability}")
            return []

        resolutions = []
        for plugin in plugins:
            resolutions.append(
                PluginResolution(
                    plugin_name=plugin.metadata.name,
                    found=True,
                    plugin=plugin,
                    capabilities=plugin.metadata.capabilities,
                )
            )

        self._logger.info(
            f"Found {len(resolutions)} plugins with capability: {capability}"
        )
        return resolutions

    def _validate_capabilities(
        self,
        plugin,
        required_capabilities: list[str],
    ) -> list[str]:
        """
        Validate that plugin has required capabilities.

        Args:
            plugin: Plugin instance to validate
            required_capabilities: List of required capabilities

        Returns:
            List of missing capabilities (empty if all present)
        """
        plugin_capabilities = set(plugin.metadata.capabilities)
        required = set(required_capabilities)
        missing = required - plugin_capabilities
        return list(missing)

    def get_available_plugins(self) -> list[str]:
        """
        Get list of all available plugin names.

        Returns:
            List of plugin names
        """
        return [p.metadata.name for p in self._registry.get_all()]

    def get_plugin_capabilities(
        self,
        plugin_name: str,
    ) -> tuple[str, ...]:
        """
        Get capabilities of a specific plugin.

        Args:
            plugin_name: Name of the plugin

        Returns:
            Tuple of capability strings

        Raises:
            PluginResolutionError: If plugin not found
        """
        if not self._registry.has_plugin(plugin_name):
            raise PluginResolutionError(
                plugin_name,
                "Plugin not found",
            )

        plugin = self._registry.get(plugin_name)
        return plugin.metadata.capabilities
