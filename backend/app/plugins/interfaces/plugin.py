"""
Purpose:
    Defines the base contract for all AgentForge plugins.

Responsibilities:
    - Define the plugin lifecycle.
    - Expose immutable plugin metadata.
    - Provide a common execution interface.

Does NOT:
    - Implement website-specific logic.
    - Access browser internals.
    - Execute browser actions directly.
"""

from abc import ABC, abstractmethod
from typing import Any

from .plugin_context import PluginContext
from .plugin_metadata import PluginMetadata


class Plugin(ABC):
    """
    Base interface that every AgentForge plugin must implement.
    """

    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """
        Return immutable metadata describing the plugin.
        """
        raise NotImplementedError

    @abstractmethod
    def initialize(self, context: PluginContext) -> None:
        """
        Initialize the plugin before execution.
        """
        raise NotImplementedError

    @abstractmethod
    def execute(self, task: Any) -> Any:
        """
        Execute a plugin-specific task.
        """
        raise NotImplementedError

    @abstractmethod
    def shutdown(self) -> None:
        """
        Release any resources held by the plugin.
        """
        raise NotImplementedError