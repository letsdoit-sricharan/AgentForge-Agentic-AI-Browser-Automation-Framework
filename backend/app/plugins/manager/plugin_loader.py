"""
Purpose:
    Dynamically load plugin modules and instantiate plugin classes.

Responsibilities:
    - Discover plugin modules in the plugins directory.
    - Dynamically import plugin modules.
    - Instantiate plugin classes.
    - Validate plugin structure.

Does NOT:
    - Register plugins.
    - Initialize plugins.
    - Execute plugins.
    - Manage plugin state.
"""

from __future__ import annotations

import importlib
import inspect
from pathlib import Path
from typing import TYPE_CHECKING

from app.plugins.exceptions import PluginLoadError, PluginValidationError
from app.plugins.interfaces import Plugin

if TYPE_CHECKING:
    pass


class PluginLoader:
    """
    Loads plugins dynamically from the plugins directory.
    """

    def __init__(
        self,
        plugins_directory: str | Path = "app/plugins",
    ) -> None:
        """
        Initialize the plugin loader.

        Args:
            plugins_directory: Path to the plugins directory.
        """
        self._plugins_dir = Path(plugins_directory)

    def discover_plugins(self) -> list[str]:
        """
        Discover all available plugin names in the plugins directory.

        Returns:
            List of plugin names (directory names).
        """
        if not self._plugins_dir.exists():
            return []

        plugin_names = []

        for item in self._plugins_dir.iterdir():
            if item.is_dir() and not item.name.startswith("_"):
                # Check if it has a plugin.py file
                plugin_file = item / "plugin.py"
                if plugin_file.exists():
                    plugin_names.append(item.name)

        return plugin_names

    def load_plugin(
        self,
        plugin_name: str,
    ) -> Plugin:
        """
        Load a plugin by name.

        Args:
            plugin_name: Name of the plugin (directory name).

        Returns:
            Instantiated Plugin instance.

        Raises:
            PluginLoadError: If plugin cannot be loaded.
            PluginValidationError: If plugin structure is invalid.
        """
        try:
            # Import the plugin module
            module_path = f"app.plugins.{plugin_name}.plugin"
            module = importlib.import_module(module_path)

        except ImportError as e:
            raise PluginLoadError(
                plugin_name,
                f"Failed to import module: {e}",
            ) from e

        # Find the Plugin class
        plugin_class = self._find_plugin_class(module, plugin_name)

        if plugin_class is None:
            raise PluginValidationError(
                plugin_name,
                [
                    "No valid Plugin class found in plugin.py",
                    "Plugin class must inherit from app.plugins.interfaces.Plugin",
                ],
            )

        # Instantiate the plugin
        try:
            plugin_instance = plugin_class()
        except Exception as e:
            raise PluginLoadError(
                plugin_name,
                f"Failed to instantiate plugin: {e}",
            ) from e

        # Validate the plugin
        self._validate_plugin(plugin_instance, plugin_name)

        return plugin_instance

    def load_all_plugins(self) -> dict[str, Plugin]:
        """
        Discover and load all available plugins.

        Returns:
            Dictionary mapping plugin names to Plugin instances.
        """
        plugin_names = self.discover_plugins()
        loaded_plugins = {}

        for plugin_name in plugin_names:
            try:
                plugin = self.load_plugin(plugin_name)
                loaded_plugins[plugin_name] = plugin
            except (PluginLoadError, PluginValidationError):
                # Skip plugins that fail to load
                # In production, this should be logged
                continue

        return loaded_plugins

    def _find_plugin_class(
        self,
        module,
        plugin_name: str,
    ) -> type[Plugin] | None:
        """
        Find the Plugin class in a module.

        Args:
            module: Imported plugin module.
            plugin_name: Name of the plugin.

        Returns:
            Plugin class or None if not found.
        """
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Check if it's a Plugin subclass (but not Plugin itself)
            if (
                issubclass(obj, Plugin)
                and obj is not Plugin
                and obj.__module__ == module.__name__
            ):
                return obj

        return None

    def _validate_plugin(
        self,
        plugin: Plugin,
        plugin_name: str,
    ) -> None:
        """
        Validate plugin structure and interface compliance.

        Args:
            plugin: Plugin instance to validate.
            plugin_name: Name of the plugin.

        Raises:
            PluginValidationError: If validation fails.
        """
        errors = []

        # Validate metadata
        try:
            metadata = plugin.metadata
            if not hasattr(metadata, "name"):
                errors.append("Plugin metadata missing 'name' attribute")
            if not hasattr(metadata, "version"):
                errors.append("Plugin metadata missing 'version' attribute")
            if not hasattr(metadata, "description"):
                errors.append("Plugin metadata missing 'description' attribute")
        except Exception as e:
            errors.append(f"Failed to access plugin metadata: {e}")

        # Validate methods
        if not callable(getattr(plugin, "initialize", None)):
            errors.append("Plugin missing 'initialize' method")
        if not callable(getattr(plugin, "execute", None)):
            errors.append("Plugin missing 'execute' method")
        if not callable(getattr(plugin, "shutdown", None)):
            errors.append("Plugin missing 'shutdown' method")

        if errors:
            raise PluginValidationError(plugin_name, errors)

    def reload_plugin(
        self,
        plugin_name: str,
    ) -> Plugin:
        """
        Reload a plugin module (useful for development).

        Args:
            plugin_name: Name of the plugin to reload.

        Returns:
            Reloaded Plugin instance.

        Raises:
            PluginLoadError: If plugin cannot be reloaded.
        """
        module_path = f"app.plugins.{plugin_name}.plugin"

        try:
            # Reload the module
            if module_path in importlib.sys.modules:
                importlib.reload(importlib.sys.modules[module_path])
        except Exception as e:
            raise PluginLoadError(
                plugin_name,
                f"Failed to reload module: {e}",
            ) from e

        # Load the plugin normally
        return self.load_plugin(plugin_name)
