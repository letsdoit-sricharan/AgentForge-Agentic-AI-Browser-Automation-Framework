"""
Execution request model.

Represents a request submitted to the Agent Runtime.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass()
class ExecutionRequest:
    """
    Represents a request submitted to the runtime.

    This object contains only information provided by the caller.
    """

    plugin: str

    workflow: str

    inputs: dict[str, Any] = field(default_factory=dict)

    priority: int = 0

    tags: list[str] = field(default_factory=list)

    correlation_id: str | None = None

    request_id: str = field(default_factory=lambda: str(uuid4()))

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
