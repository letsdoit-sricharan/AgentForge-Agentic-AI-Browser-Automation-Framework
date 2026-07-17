"""
Workflow event model.

Represents workflow-related events emitted by the
Agent Runtime.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from app.runtime.events.event_types import WorkflowEventType


@dataclass(frozen=True)
class WorkflowEvent:
    """
    Immutable workflow event.

    Represents workflow and task lifecycle events.
    """

    event_type: WorkflowEventType

    execution_id: str

    workflow_id: str

    source: str

    task_name: str | None = None

    payload: dict[str, Any] = field(default_factory=dict)

    event_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    @property
    def name(self) -> str:
        """
        Human-readable event name.
        """
        return self.event_type.value