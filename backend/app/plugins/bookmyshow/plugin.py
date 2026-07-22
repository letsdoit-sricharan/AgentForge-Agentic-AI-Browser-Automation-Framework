"""
Purpose:
    BookMyShow plugin implementation.

Responsibilities:
    - Execute the BookMyShow booking workflow.
    - Validate the workflow input.
    - Return a structured workflow result.

Does NOT:
    - Create WorkflowContext objects.
    - Manage browser lifecycle.
    - Import Playwright.
    - Contain browser automation logic.
"""

from __future__ import annotations

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
        self.workflows = {
            "booking_workflow": self._workflow
        }

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
        context: WorkflowContext,
    ):
        """
        Execute the booking workflow.
        """

        if self._context is None:
            raise RuntimeError(
                "Plugin has not been initialized."
            )

        request = context.input_data.get(
            "booking_request",
        )

        if not isinstance(
            request,
            BookingRequest,
        ):
            raise TypeError(
                "Expected BookingRequest."
            )

        return await self._workflow.execute(
            context,
        )

    def shutdown(self) -> None:
        """
        Shutdown the plugin.
        """
        self._context = None