"""
Execution request.

Represents a single runtime execution request.

Responsibilities:
    - Identify the plugin to execute.
    - Carry the plugin context.
    - Carry the workflow input.

Does NOT:
    - Execute plugins.
    - Manage browser resources.
    - Contain runtime logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.plugins.interfaces.plugin import Plugin
from app.plugins.interfaces.plugin_context import PluginContext


@dataclass
class ExecutionRequest:
    """
    Represents a single plugin execution request.
    """

    plugin: Plugin

    plugin_context: PluginContext

    task: Any