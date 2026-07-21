"""
Purpose:
    Defines the controlled execution context provided to plugins.

Responsibilities:
    - Expose approved framework services.
    - Isolate plugins from framework internals.
    - Act as the plugin's gateway into AgentForge.

Does NOT:
    - Execute workflows.
    - Manage browser lifecycle.
    - Store plugin state.
    - Expose Playwright or browser internals.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class PluginContext:
    """
    Context object supplied to every plugin.
    """

    runtime: Any
    actions: Any
    memory: Any
    configuration: Any
    logger: Any