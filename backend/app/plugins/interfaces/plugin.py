"""
Purpose:
    Defines the base interface implemented by all AgentForge plugins.

Responsibilities:
    - Expose immutable plugin metadata.
    - Support initialization and shutdown.
    - Execute workflows using a WorkflowContext.

Does NOT:
    - Manage browser lifecycle.
    - Create WorkflowContext instances.
    - Import Playwright.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.plugin_framework.plugin_context import PluginContext
from app.plugin_framework.workflow.workflow_context import WorkflowContext


class Plugin(ABC):
    """
    Base interface implemented by every AgentForge plugin.
    """

    @property
    @abstractmethod
    def metadata(self):
        """
        Return immutable plugin metadata.
        """
        raise NotImplementedError

    @abstractmethod
    def initialize(
        self,
        context: PluginContext,
    ) -> None:
        """
        Initialize the plugin.
        """
        raise NotImplementedError

    @abstractmethod
    async def execute(
        self,
        context: WorkflowContext,
    ):
        """
        Execute the plugin using the supplied workflow context.
        """
        raise NotImplementedError

    @abstractmethod
    def shutdown(self) -> None:
        """
        Shutdown the plugin.
        """
        raise NotImplementedError
