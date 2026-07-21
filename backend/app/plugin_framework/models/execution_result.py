"""
Purpose:
    Represents the overall execution result of a workflow.

Responsibilities:
    - Store workflow execution status.
    - Wrap the WorkflowResult.
    - Provide framework-level execution information.

Does NOT:
    - Execute workflows.
    - Import Playwright.
    - Contain website-specific logic.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.plugin_framework.models.workflow_status import WorkflowStatus
from app.plugin_framework.workflow.workflow_result import WorkflowResult


@dataclass
class ExecutionResult:
    """
    Represents the framework-level execution result of a workflow.
    """

    status: WorkflowStatus

    workflow_result: WorkflowResult

    message: str = ""