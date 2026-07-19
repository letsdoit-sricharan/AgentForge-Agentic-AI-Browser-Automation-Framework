"""
Purpose:
    Defines the abstract base class for plugin workflows.

Responsibilities:
    - Maintain an ordered collection of workflow steps.
    - Define the workflow execution contract.
    - Provide reusable step management.

Does NOT:
    - Execute browser operations.
    - Import Playwright.
    - Contain website-specific logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TYPE_CHECKING

from app.plugin_framework.steps.workflow_step import WorkflowStep

if TYPE_CHECKING:
    from app.plugin_framework.workflow.workflow_context import WorkflowContext
    from app.plugin_framework.workflow.workflow_result import WorkflowResult


class Workflow(ABC):
    """
    Base class for all plugin workflows.
    """

    def __init__(self) -> None:
        self._steps: list[WorkflowStep] = []

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Return the workflow name.
        """

    @property
    def steps(self) -> Sequence[WorkflowStep]:
        """
        Return all workflow steps.
        """

        return tuple(self._steps)

    def add_step(
        self,
        step: WorkflowStep,
    ) -> None:
        """
        Add a workflow step.
        """

        self._steps.append(step)

    def clear_steps(self) -> None:
        """
        Remove all workflow steps.
        """

        self._steps.clear()

    @abstractmethod
    def execute(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult:
        """
        Execute the workflow.

        Args:
            context:
                Workflow execution context.

        Returns:
            WorkflowResult
        """