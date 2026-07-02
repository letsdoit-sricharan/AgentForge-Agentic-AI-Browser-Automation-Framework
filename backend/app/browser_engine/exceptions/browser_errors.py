"""
Purpose:
    Define base exception classes for the Browser Engine components.

Responsibilities:
    - Establish a custom error hierarchy starting with BrowserEngineError.

Must NOT do:
    - Expose library-specific exception objects (e.g. Playwright Error).
"""

from __future__ import annotations
from typing import Optional


class BrowserEngineError(Exception):
    """
    Base exception for all errors raised within the Browser Engine package.
    """
    def __init__(self, message: str, original_error: Optional[Exception] = None) -> None:
        super().__init__(message)
        self.original_error = original_error
