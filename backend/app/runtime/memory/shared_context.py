"""
Shared runtime context.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.runtime.state.execution_state import ExecutionState
from app.runtime.state.workflow_state import WorkflowState

from .runtime_memory import RuntimeMemory


@dataclass()
class SharedContext:
    """
    Shared context available to runtime components.
    """

    execution_state: ExecutionState

    workflow_state: WorkflowState

    memory: RuntimeMemory
