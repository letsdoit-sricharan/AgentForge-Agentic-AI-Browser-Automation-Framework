"""
Purpose:
    BookMyShow plugin implementation.

Responsibilities:
    - Accept booking requests.
    - Execute the BookMyShow booking workflow.
    - Return a structured booking result.

Does NOT:
    - Perform browser automation directly.
    - Import Playwright.
    - Contain page-specific logic.
"""

from __future__ import annotations

from typing import Any

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.interfaces.plugin import Plugin
from app.plugins.interfaces.plugin_context import PluginContext

from .metadata import METADATA
from .models.booking_request import BookingRequest
from .workflows.booking_workflow import BookingWorkflow


class BookMyShowPlugin(Plugin):
    """
    Reference implementation of the BookMyShow plugin.
    """

    def __init__(self) -> None:
        self._context: PluginContext | None = None
        self._workflow = BookingWorkflow()

    @property
    def metadata(self):
        """
        Return immutable plugin metadata.
        """
        return METADATA

    def initialize(
        self,
        context: PluginContext,
    ) -> None:
        """
        Initialize the plugin.
        """
        self._context = context

    async def execute(
        self,
        task: Any,
    ) -> Any:
        """
        Execute a booking request.
        """

        if self._context is None:
            raise RuntimeError(
                "Plugin has not been initialized."
            )

        if not isinstance(task, BookingRequest):
            raise TypeError(
                "Expected BookingRequest."
            )

        workflow_context = WorkflowContext(
            plugin_context=self._context,
            input_data={
                "booking_request": task,
            },
        )

        return await self._workflow.execute(
            workflow_context,
        )

    def shutdown(self) -> None:
        """
        Shutdown the plugin.
        """
        self._context = None