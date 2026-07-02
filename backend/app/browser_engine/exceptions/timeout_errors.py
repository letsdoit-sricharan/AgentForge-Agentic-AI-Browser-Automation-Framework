"""
Purpose:
    Define timeout-specific exception classes for the Browser Engine.

Responsibilities:
    - Define BrowserTimeoutError subclassing BrowserEngineError.

Must NOT do:
    - Expose library-specific timeout exception objects.
"""

from __future__ import annotations
from app.browser_engine.exceptions.browser_errors import BrowserEngineError


class BrowserTimeoutError(BrowserEngineError):
    """
    Exception raised when a browser operation (e.g. wait for element, page load) times out.
    """
    pass
