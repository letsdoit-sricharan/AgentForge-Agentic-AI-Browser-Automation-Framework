"""
Shared runtime context.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.runtime.state import ExecutionState, WorkflowState

from .runtime_memory import RuntimeMemory


@dataclass(slots=True)
class SharedContext:
    """
    Shared context available to runtime components.
    """

    execution_state: ExecutionState

    workflow_state: WorkflowState

    memory: RuntimeMemory