"""
Task Metadata

Descriptive information about task types.

Responsibilities:
    - Describe task capabilities
    - Define task requirements
    - Provide task documentation
    - Support task discovery

Does NOT:
    - Execute tasks
    - Contain business logic
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class TaskMetadata:
    """
    Metadata describing a task type.

    Used by:
    - TaskRegistry to catalog supported tasks
    - AI Planner to understand task requirements
    - Task discovery and documentation
    """

    # Task identification
    task_type: str
    name: str
    description: str

    # Task categorization
    category: str = "general"  # e.g., "search", "selection", "transaction"

    # Required input fields
    required_inputs: tuple[str, ...] = field(default_factory=tuple)

    # Optional input fields
    optional_inputs: tuple[str, ...] = field(default_factory=tuple)

    # Expected output fields
    output_fields: tuple[str, ...] = field(default_factory=tuple)

    # Task capabilities (what it requires)
    capabilities: tuple[str, ...] = field(default_factory=tuple)

    # Estimated execution time (seconds)
    estimated_duration: float | None = None

    # Can this task be retried safely?
    idempotent: bool = True

    # Additional metadata
    metadata: dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        """String representation."""
        return f"TaskMetadata(task_type={self.task_type}, name={self.name})"
