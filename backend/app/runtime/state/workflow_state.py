"""
Workflow state model.

Tracks the progress of a workflow execution.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True)
class WorkflowState:
    """
    Represents the progress of a workflow execution.

    This class is responsible only for tracking workflow progress.
    It does not execute workflow steps.
    """

    workflow_id: str

    total_steps: int

    completed_steps: int = 0

    current_step: str | None = None

    failed_step: str | None = None

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    @property
    def progress(self) -> float:
        """
        Returns workflow completion as a percentage.

        Returns:
            float: Progress in the range [0.0, 100.0].
        """
        if self.total_steps == 0:
            return 0.0

        return (self.completed_steps / self.total_steps) * 100

    @property
    def is_complete(self) -> bool:
        """
        Returns True if all workflow steps have completed.
        """
        return self.completed_steps >= self.total_steps

    def set_current_step(
        self,
        step_name: str | None,
    ) -> None:
        """
        Updates the currently executing workflow step.
        """
        self.current_step = step_name
        self.updated_at = datetime.now(UTC)

    def complete_step(self) -> None:
        """
        Marks the current workflow step as completed.
        """
        if self.completed_steps < self.total_steps:
            self.completed_steps += 1

        self.updated_at = datetime.now(UTC)

    def set_failed_step(
        self,
        step_name: str,
    ) -> None:
        """
        Records the step that caused workflow failure.
        """
        self.failed_step = step_name
        self.updated_at = datetime.now(UTC)