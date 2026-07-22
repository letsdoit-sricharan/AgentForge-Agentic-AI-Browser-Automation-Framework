"""
Purpose:
    Defines the reusable base class for all BookMyShow workflow steps.

Responsibilities:
    - Provide common execution flow.
    - Standardize success/error handling.
    - Reduce duplicate code.

Does NOT:
    - Perform browser automation.
    - Import Playwright.
    - Contain page-specific logic.
"""

from __future__ import annotations

from abc import abstractmethod

from app.plugin_framework.steps.step_result import StepResult
from app.plugin_framework.steps.workflow_step import WorkflowStep
from app.plugin_framework.workflow.workflow_context import WorkflowContext


class BaseBookMyShowStep(WorkflowStep):
    """
    Base class for all BookMyShow workflow steps.
    """

    @property
    @abstractmethod
    def success_message(self) -> str:
        """
        Message returned when the step succeeds.
        """

    @abstractmethod
    async def perform(
        self,
        context: WorkflowContext,
    ) -> None:
        """
        Perform the actual step logic.
        """

    async def execute(
        self,
        context: WorkflowContext,
    ) -> StepResult:
        """
        Execute the workflow step.
        """

        try:

            await self.perform(
                context,
            )

            return StepResult(
                success=True,
                message=self.success_message,
            )

        except Exception as exc:

            return StepResult(
                success=False,
                message=str(exc),
            )