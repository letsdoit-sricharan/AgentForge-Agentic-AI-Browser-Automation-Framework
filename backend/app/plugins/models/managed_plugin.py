"""
Purpose:
    Represents a managed plugin within the AgentForge Plugin Infrastructure.

Responsibilities:
    - Store the runtime information of a plugin.
    - Track plugin lifecycle state.
    - Store execution statistics.
    - Store runtime context.

Does NOT:
    - Execute plugins.
    - Manage lifecycle.
    - Perform browser automation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.plugins.interfaces import Plugin, PluginContext
from app.plugins.models.plugin_state import PluginStatus


@dataclass
class ManagedPlugin:
    """
    Represents a plugin managed by the Plugin Infrastructure.
    """

    plugin: Plugin

    status: PluginStatus = PluginStatus.UNLOADED

    context: PluginContext | None = None

    initialized_at: datetime | None = None

    last_execution_at: datetime | None = None

    execution_count: int = 0

    last_error: Exception | None = None

    created_at: datetime = field(default_factory=datetime.utcnow)
