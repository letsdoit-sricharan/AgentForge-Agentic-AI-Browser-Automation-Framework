"""
Execution metadata.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


@dataclass()
class ExecutionMetadata:
    """
    Runtime-generated metadata.

    This object is created by the runtime after an
    execution request is accepted.
    """

    execution_id: str = field(default_factory=lambda: str(uuid4()))

    started_at: datetime | None = None

    completed_at: datetime | None = None

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    source: str = "runtime"

    worker_id: str | None = None

    parent_execution_id: str | None = None

    retry_attempt: int = 0