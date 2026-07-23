"""
Purpose:
    Defines the execution states of a workflow.

Responsibilities:
    - Represent the lifecycle of a workflow.
    - Provide strongly typed workflow states.

Does NOT:
    - Execute workflow logic.
    - Store workflow data.
    - Import Playwright.
"""

from __future__ import annotations

from enum import Enum


class WorkflowStatus(str, Enum):
    """
    Represents the lifecycle status of a workflow.
    """

    CREATED = "created"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"
