"""
Plugin manager.

Owns all plugins registered with the runtime.
"""

from __future__ import annotations

from app.plugins.interfaces.plugin import Plugin
from app.plugins.interfaces.plugin_context import PluginContext


class PluginManager:
    """
    Manages plugin lifecycle.
    """

    def __init__(self) -> None:
        self._plugins: dict[str, Plugin] = {}

    def register(
        self,
        plugin: Plugin,
    ) -> None:
        """
        Register a plugin.
        """
        name = plugin.metadata.name

        self._plugins[name] = plugin

    def get(
        self,
        name: str,
    ) -> Plugin:
        """
        Retrieve a registered plugin.
        """
        try:
            return self._plugins[name]

        except KeyError as exc:
            raise ValueError(
                f"Unknown plugin '{name}'."
            ) from exc

    def initialize(
        self,
        name: str,
        context: PluginContext,
    ) -> Plugin:
        """
        Initialize a registered plugin.
        """
        plugin = self.get(name)

        plugin.initialize(context)

        return plugin

    def shutdown(
        self,
        name: str,
    ) -> None:
        """
        Shutdown a plugin.
        """
        self.get(name).shutdown()

    @property
    def plugins(self) -> tuple[Plugin, ...]:
        """
        Return all registered plugins.
        """
        return tuple(self._plugins.values())
