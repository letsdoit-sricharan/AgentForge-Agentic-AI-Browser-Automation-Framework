"""
Execution context.

Shared execution context passed throughout the Agent Runtime.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.runtime.execution.execution_metadata import ExecutionMetadata
from app.runtime.execution.execution_request import ExecutionRequest
from app.runtime.memory.runtime_memory import RuntimeMemory
from app.runtime.state.execution_state import ExecutionState
from app.runtime.state.execution_status import ExecutionStatus
from app.runtime.state.workflow_state import WorkflowState


@dataclass(slots=True)
class ExecutionContext:
    """
    Shared execution context.

    This object aggregates all state required for a single
    execution and is passed between runtime components.
    """

    request: ExecutionRequest

    metadata: ExecutionMetadata

    execution_state: ExecutionState

    workflow_state: WorkflowState

    memory: RuntimeMemory

    # ------------------------------------------------------------------
    # Convenience Properties
    # ------------------------------------------------------------------

    @property
    def execution_id(self) -> str:
        """Unique runtime execution identifier."""
        return self.metadata.execution_id

    @property
    def request_id(self) -> str:
        """Original request identifier."""
        return self.request.request_id

    @property
    def plugin(self) -> str:
        """Target plugin."""
        return self.request.plugin

    @property
    def workflow(self) -> str:
        """Workflow name."""
        return self.request.workflow

    @property
    def status(self) -> ExecutionStatus:
        """Current execution status."""
        return self.execution_state.status

    @property
    def current_step(self) -> str | None:
        """Current workflow step."""
        return self.workflow_state.current_step

    @property
    def progress(self) -> float:
        """Workflow completion percentage."""
        return self.workflow_state.progress

    @property
    def retry_count(self) -> int:
        """Current retry attempt."""
        return self.execution_state.retry_count