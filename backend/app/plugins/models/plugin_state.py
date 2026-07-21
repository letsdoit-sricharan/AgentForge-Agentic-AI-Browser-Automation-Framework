"""
Purpose:
    Defines plugin lifecycle state.

Responsibilities:
    - Track plugin state transitions.
    - Provide state validation.
    - Support plugin lifecycle management.

Does NOT:
    - Execute plugins.
    - Manage plugin instances.
    - Handle state persistence.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any


class PluginStatus(Enum):
    """Plugin lifecycle status."""

    UNLOADED = auto()
    LOADING = auto()
    LOADED = auto()
    INITIALIZING = auto()
    READY = auto()
    EXECUTING = auto()
    ERROR = auto()
    SHUTTING_DOWN = auto()
    SHUTDOWN = auto()


@dataclass
class PluginState:
    """
    Represents the runtime state of a plugin.
    """

    plugin_name: str
    status: PluginStatus = PluginStatus.UNLOADED
    error: Exception | None = None
    loaded_at: datetime | None = None
    initialized_at: datetime | None = None
    last_executed_at: datetime | None = None
    execution_count: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def can_initialize(self) -> bool:
        """Check if plugin can be initialized."""
        return self.status == PluginStatus.LOADED

    def can_execute(self) -> bool:
        """Check if plugin can execute."""
        return self.status == PluginStatus.READY

    def can_shutdown(self) -> bool:
        """Check if plugin can be shut down."""
        return self.status in (
            PluginStatus.READY,
            PluginStatus.ERROR,
        )

    def mark_loading(self) -> None:
        """Mark plugin as loading."""
        self.status = PluginStatus.LOADING
        self.error = None

    def mark_loaded(self) -> None:
        """Mark plugin as loaded."""
        self.status = PluginStatus.LOADED
        self.loaded_at = datetime.now()
        self.error = None

    def mark_initializing(self) -> None:
        """Mark plugin as initializing."""
        self.status = PluginStatus.INITIALIZING
        self.error = None

    def mark_ready(self) -> None:
        """Mark plugin as ready."""
        self.status = PluginStatus.READY
        self.initialized_at = datetime.now()
        self.error = None

    def mark_executing(self) -> None:
        """Mark plugin as executing."""
        self.status = PluginStatus.EXECUTING
        self.error = None

    def mark_execution_complete(self) -> None:
        """Mark plugin execution as complete."""
        self.status = PluginStatus.READY
        self.last_executed_at = datetime.now()
        self.execution_count += 1
        self.error = None

    def mark_error(self, error: Exception) -> None:
        """Mark plugin as errored."""
        self.status = PluginStatus.ERROR
        self.error = error

    def mark_shutting_down(self) -> None:
        """Mark plugin as shutting down."""
        self.status = PluginStatus.SHUTTING_DOWN
        self.error = None

    def mark_shutdown(self) -> None:
        """Mark plugin as shut down."""
        self.status = PluginStatus.SHUTDOWN
        self.error = None
