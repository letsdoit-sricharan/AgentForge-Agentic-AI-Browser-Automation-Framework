"""
Purpose:
    Defines timeout-related exceptions for the Browser Engine.

Responsibilities:
    - Represent timeout failures.
    - Provide browser-engine-specific timeout exceptions.

Must NOT do:
    - Import Playwright.
    - Implement timeout logic.
"""

from app.browser_engine.exceptions.browser_errors import BrowserEngineError


class BrowserTimeoutError(BrowserEngineError):
    """
    Base exception for all Browser Engine timeout errors.
    """
    pass


class NavigationTimeoutError(BrowserTimeoutError):
    """
    Raised when page navigation exceeds the configured timeout.
    """
    pass


class ElementTimeoutError(BrowserTimeoutError):
    """
    Raised when waiting for an element exceeds the configured timeout.
    """
    pass
