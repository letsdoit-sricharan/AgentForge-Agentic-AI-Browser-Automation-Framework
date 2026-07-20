"""
Purpose:
    Defines the reusable base class for all BookMyShow workflow steps.

Responsibilities:
    - Provide common placeholder execution logic.
    - Enforce a consistent step interface.
    - Reduce duplicate code across workflow steps.

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

    async def execute(
        self,
        context: WorkflowContext,
    ) -> StepResult:
        """
        Execute the workflow step.

        Version 1.0:
        Returns a successful placeholder result.
        """

        return StepResult(
            success=True,
            message=self.success_message,
        )