"""
Purpose:
    Entry point for the BookMyShow plugin.

Responsibilities:
    - Implement the AgentForge Plugin interface.
    - Execute the BookMyShow booking workflow.
    - Convert workflow results into booking results.

Does NOT:
    - Perform browser automation.
    - Import Playwright.
    - Contain workflow logic.
"""

from __future__ import annotations

from typing import Any

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.bookmyshow.metadata import BOOKMYSHOW_METADATA
from app.plugins.bookmyshow.models.booking_request import BookingRequest
from app.plugins.bookmyshow.models.booking_result import BookingResult
from app.plugins.bookmyshow.workflows.booking_workflow import BookingWorkflow
from app.plugins.interfaces import Plugin, PluginContext, PluginMetadata


class BookMyShowPlugin(Plugin):
    """
    AgentForge BookMyShow plugin.
    """

    def __init__(self) -> None:
        self._context: PluginContext | None = None
        self._workflow = BookingWorkflow()

    @property
    def metadata(self) -> PluginMetadata:
        """
        Return plugin metadata.
        """
        return BOOKMYSHOW_METADATA

    def initialize(
        self,
        context: PluginContext,
    ) -> None:
        """
        Initialize the plugin.
        """
        self._context = context

    def execute(
        self,
        task: Any,
    ) -> BookingResult:
        """
        Execute a booking request.
        """

        if self._context is None:
            raise RuntimeError(
                "Plugin has not been initialized."
            )

        if not isinstance(task, BookingRequest):
            raise TypeError(
                "Expected a BookingRequest."
            )

        workflow_context = WorkflowContext(
            plugin_context=self._context,
            input_data={
                "booking_request": task,
            },
        )

        workflow_result = self._workflow.execute(
            workflow_context,
        )

        return BookingResult(
            success=workflow_result.success,
            message=workflow_result.message,
        )

    def shutdown(self) -> None:
        """
        Shutdown the plugin.
        """
        self._context = None