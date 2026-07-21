"""
Task Context

Execution context for tasks.

Responsibilities:
    - Provide task execution information
    - Store task input data
    - Track correlation and metadata
    - Remain browser-independent

Does NOT:
    - Contain browser objects (Session, Page, etc.)
    - Execute browser operations
    - Know about plugins or workflows
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class TaskContext:
    """
    Context for task execution.
    
    Separates business-level execution context (task) from
    technical execution context (workflow/browser).
    
    TaskContext → Converted to → WorkflowContext (by TaskExecutor)
    """

    # Task identification
    task_id: str
    task_type: str
    
    # Task input data
    input_data: dict[str, Any] = field(default_factory=dict)
    
    # Execution metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    priority: int = 0
    
    # Correlation for tracking related tasks
    correlation_id: str | None = None
    parent_task_id: str | None = None
    
    # Configuration
    configuration: dict[str, Any] = field(default_factory=dict)
    
    # Timeout in seconds
    timeout: float | None = None
    
    # Retry configuration
    max_retries: int = 0
    retry_count: int = 0
    
    # Additional metadata
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "input_data": self.input_data,
            "created_at": self.created_at.isoformat(),
            "priority": self.priority,
            "correlation_id": self.correlation_id,
            "parent_task_id": self.parent_task_id,
            "configuration": self.configuration,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "retry_count": self.retry_count,
            "metadata": self.metadata,
        }
