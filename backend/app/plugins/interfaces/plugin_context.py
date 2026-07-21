"""
Purpose:
    Re-exports PluginContext for backward compatibility.

    The canonical definition has moved to app.plugin_framework.plugin_context
    to break the circular dependency between plugin_framework and plugins.

    All existing imports from this module continue to work unchanged.
"""

from app.plugin_framework.plugin_context import PluginContext  # noqa: F401

__all__ = ["PluginContext"]