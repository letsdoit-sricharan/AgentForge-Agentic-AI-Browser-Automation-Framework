"""
Plugin Framework step abstractions.
"""

from .step_result import StepResult
from .workflow_step import WorkflowStep

__all__ = [
    "WorkflowStep",
    "StepResult",
]