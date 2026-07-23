"""
Purpose:
    Represents the result of executing a single workflow step.

Responsibilities:
    - Indicate whether the step succeeded.
    - Store step output data.
    - Store execution messages.
    - Store execution errors.

Does NOT:
    - Execute step logic.
    - Import Playwright.
    - Contain website-specific logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class StepResult:
    """
    Represents the outcome of a workflow step.
    """

    success: bool

    message: str = ""

    data: dict[str, Any] = field(default_factory=dict)

    error: Exception | None = None
