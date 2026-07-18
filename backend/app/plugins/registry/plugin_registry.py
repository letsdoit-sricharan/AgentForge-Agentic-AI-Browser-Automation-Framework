"""
Purpose:
    Maintains the registry of all managed plugins.

Responsibilities:
    - Register plugins.
    - Remove plugins.
    - Retrieve managed plugins.
    - List registered plugins.

Does NOT:
    - Load plugins.
    - Execute plugins.
    - Manage plugin lifecycle.
"""

from __future__ import annotations

from typing import Dict, List

from app.plugins.exceptions import PluginRegistrationError
from app.plugins.interfaces import Plugin
from app.plugins.models import ManagedPlugin


class PluginRegistry:
    """
    Stores all registered plugins as ManagedPlugin instances.
    """

    def __init__(self) -> None:
        self._plugins: Dict[str, ManagedPlugin] = {}

    def register(self, plugin: Plugin) -> ManagedPlugin:
        """
        Register a plugin.

        Returns the created ManagedPlugin.
        """

        name = plugin.metadata.name

        if name in self._plugins:
            raise PluginRegistrationError(
                f"Plugin '{name}' is already registered."
            )

        managed = ManagedPlugin(plugin=plugin)

        self._plugins[name] = managed

        return managed

    def unregister(self, name: str) -> None:
        """
        Remove a plugin.
        """

        self._plugins.pop(name, None)

    def get(self, name: str) -> ManagedPlugin:
        """
        Retrieve a managed plugin.
        """

        try:
            return self._plugins[name]
        except KeyError as exc:
            raise PluginRegistrationError(
                f"Plugin '{name}' is not registered."
            ) from exc

    def exists(self, name: str) -> bool:
        """
        Check if a plugin exists.
        """

        return name in self._plugins

    def list_plugins(self) -> List[str]:
        """
        Return registered plugin names.
        """

        return sorted(self._plugins.keys())

    def clear(self) -> None:
        """
        Remove every registered plugin.
        """

        self._plugins.clear()