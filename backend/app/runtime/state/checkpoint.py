"""
Checkpoint model.

Represents a serializable snapshot of runtime execution.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from .execution_state import ExecutionState
from .workflow_state import WorkflowState


@dataclass()
class Checkpoint:
    """
    Represents a snapshot of runtime state.

    A checkpoint is intended for pause/resume, recovery,
    or persistence. It contains only execution state and
    workflow progress information.
    """

    checkpoint_id: str

    execution_state: ExecutionState

    workflow_state: WorkflowState

    version: int = 1

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )