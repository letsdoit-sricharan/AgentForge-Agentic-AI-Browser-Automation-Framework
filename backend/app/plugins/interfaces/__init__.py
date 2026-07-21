"""Plugin interfaces."""

from app.plugins.interfaces.plugin import Plugin
from app.plugins.interfaces.plugin_context import PluginContext
from app.plugins.interfaces.plugin_metadata import PluginMetadata

__all__ = [
    "Plugin",
    "PluginContext",
    "PluginMetadata",
]
