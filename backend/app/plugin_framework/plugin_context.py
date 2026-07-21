"""
Purpose:
    Defines the controlled execution context provided to plugins.

Responsibilities:
    - Expose approved framework services to plugins.
    - Isolate plugins from framework internals.
    - Act as the plugin's gateway into AgentForge.

Location rationale:
    PluginContext is a framework-level concept: it is created by the
    framework and passed into plugins.  It lives here in plugin_framework
    (not in the plugins package) so that plugin_framework can reference
    it without importing from plugins, eliminating the circular dependency:

        plugin_framework.workflow.workflow_context
            → plugins.interfaces.plugin_context   (OLD — caused cycle)

        plugin_framework.plugin_context            (NEW — no cycle)

Does NOT:
    - Execute workflows.
    - Manage browser lifecycle.
    - Store plugin state.
    - Expose Playwright or browser internals.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class PluginContext:
    """
    Context object supplied to every plugin during initialization and execution.

    The framework constructs a PluginContext and hands it to each plugin via
    Plugin.initialize().  Plugins must not retain references to framework
    internals beyond what is exposed here.
    """

    runtime: Any
    actions: Any
    memory: Any
    configuration: Any
    logger: Any
