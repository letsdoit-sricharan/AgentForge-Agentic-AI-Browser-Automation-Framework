"""
Purpose:
    Represents the result of validating workflow data.

Responsibilities:
    - Indicate whether validation succeeded.
    - Provide validation messages.
    - Store optional validation details.

Does NOT:
    - Perform validation.
    - Execute browser operations.
    - Import Playwright.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ValidationResult:
    """
    Represents the outcome of a validation operation.
    """

    valid: bool

    message: str = ""

    details: dict[str, Any] = field(default_factory=dict)