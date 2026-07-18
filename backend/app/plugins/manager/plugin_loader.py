"""
Purpose:
    Responsible for loading and registering AgentForge plugins.

Responsibilities:
    - Instantiate plugin classes.
    - Validate plugins.
    - Register plugins with the PluginRegistry.

Does NOT:
    - Execute plugins.
    - Manage plugin lifecycle.
    - Access browser internals.
"""

from __future__ import annotations

from typing import Sequence, Type

from app.plugins.exceptions import PluginValidationError
from app.plugins.interfaces import Plugin
from app.plugins.models import ManagedPlugin
from app.plugins.registry import PluginRegistry


class PluginLoader:
    """
    Loads plugins into the PluginRegistry.
    """

    def __init__(self, registry: PluginRegistry) -> None:
        self._registry = registry

    def load(
        self,
        plugin_class: Type[Plugin],
    ) -> ManagedPlugin:
        """
        Instantiate, validate, and register a plugin.

        Returns:
            ManagedPlugin: The registered managed plugin.
        """

        plugin = plugin_class()

        self._validate(plugin)

        managed_plugin = self._registry.register(plugin)

        return managed_plugin

    def load_many(
        self,
        plugin_classes: Sequence[Type[Plugin]],
    ) -> list[ManagedPlugin]:
        """
        Load and register multiple plugins.
        """

        managed_plugins: list[ManagedPlugin] = []

        for plugin_class in plugin_classes:
            managed_plugins.append(self.load(plugin_class))

        return managed_plugins

    def discover(self) -> None:
        """
        Placeholder for future automatic plugin discovery.

        Version 1.0 intentionally uses explicit loading.
        """

        raise NotImplementedError(
            "Automatic plugin discovery is not implemented."
        )

    @staticmethod
    def _validate(plugin: Plugin) -> None:
        """
        Validate a plugin before registration.
        """

        metadata = plugin.metadata

        if not metadata.name.strip():
            raise PluginValidationError(
                "Plugin name cannot be empty."
            )

        if not metadata.version.strip():
            raise PluginValidationError(
                "Plugin version cannot be empty."
            )