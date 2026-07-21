"""Plugin exceptions."""

from app.plugins.exceptions.plugin_errors import (
    PluginAlreadyRegisteredError,
    PluginDependencyError,
    PluginError,
    PluginExecutionError,
    PluginInitializationError,
    PluginLoadError,
    PluginNotFoundError,
    PluginRegistrationError,
    PluginStateError,
    PluginValidationError,
)

__all__ = [
    "PluginError",
    "PluginNotFoundError",
    "PluginAlreadyRegisteredError",
    "PluginRegistrationError",  # backward-compatible alias
    "PluginLoadError",
    "PluginInitializationError",
    "PluginExecutionError",
    "PluginValidationError",
    "PluginStateError",
    "PluginDependencyError",
]
