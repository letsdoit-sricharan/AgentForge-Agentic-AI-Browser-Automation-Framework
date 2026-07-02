"""
Purpose:
    Define navigation-specific exception classes for the Browser Engine.

Responsibilities:
    - Define BrowserNavigationError subclassing BrowserEngineError.

Must NOT do:
    - Expose library-specific navigation exception objects.
"""

from __future__ import annotations
from app.browser_engine.exceptions.browser_errors import BrowserEngineError


class BrowserNavigationError(BrowserEngineError):
    """
    Exception raised when a page navigation fails (e.g. invalid URL, network down, SSL failure).
    """
    pass
