"""
Purpose:
    Defines the abstract base class for all validators.

Responsibilities:
    - Define the validation contract.
    - Validate workflow data.
    - Return a ValidationResult.

Does NOT:
    - Execute browser operations.
    - Import Playwright.
    - Modify workflow data.
    - Contain website-specific logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from app.plugin_framework.validators.validation_result import ValidationResult


class Validator(ABC):
    """
    Abstract base class for all validators.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Return the unique validator name.
        """

    @abstractmethod
    def validate(
        self,
        data: Any,
    ) -> ValidationResult:
        """
        Validate the supplied data.

        Args:
            data:
                The object to validate.

        Returns:
            ValidationResult
        """
