"""
Purpose:
    Defines navigation-related exceptions for the Browser Engine.

Responsibilities:
    - Represent page navigation failures.
    - Abstract browser-specific navigation exceptions.

Must NOT do:
    - Import Playwright.
    - Perform navigation.
"""

from app.browser_engine.exceptions.browser_errors import BrowserEngineError


class NavigationError(BrowserEngineError):
    """
    Raised when page navigation fails.
    """

    pass


class InvalidUrlError(NavigationError):
    """
    Raised when an invalid URL is provided.
    """

    pass


class PageLoadError(NavigationError):
    """
    Raised when a page fails to load successfully.
    """

    pass