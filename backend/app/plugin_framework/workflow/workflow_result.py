"""
Purpose:
    Represents the result of a workflow execution.

Responsibilities:
    - Indicate whether the workflow succeeded.
    - Store execution data.
    - Store execution messages.
    - Store execution errors.

Does NOT:
    - Execute workflow logic.
    - Import Playwright.
    - Contain website-specific information.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class WorkflowResult:
    """
    Represents the outcome of a workflow execution.
    """

    success: bool

    message: str = ""

    data: dict[str, Any] = field(default_factory=dict)

    error: Exception | None = None
