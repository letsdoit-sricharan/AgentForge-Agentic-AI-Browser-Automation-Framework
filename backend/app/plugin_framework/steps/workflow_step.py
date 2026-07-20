"""
Purpose:
    Defines the abstract base class for workflow steps.

Responsibilities:
    - Define the contract for a single workflow step.
    - Execute one unit of work.
    - Return a StepResult.

Does NOT:
    - Execute complete workflows.
    - Import Playwright.
    - Manage retries.
    - Contain website-specific logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from app.plugin_framework.steps.step_result import StepResult

if TYPE_CHECKING:
    from app.plugin_framework.workflow.workflow_context import WorkflowContext


class WorkflowStep(ABC):
    """
    Abstract base class for all workflow steps.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Return the unique step name.
        """

    @abstractmethod
    async def execute(
        self,
        context: WorkflowContext,
    ) -> StepResult:
        """
        Execute this workflow step.

        Args:
            context:
                Workflow execution context.

        Returns:
            StepResult
        """