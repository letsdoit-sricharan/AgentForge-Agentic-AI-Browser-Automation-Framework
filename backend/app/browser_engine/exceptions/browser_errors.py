"""
Purpose:
    Defines the base exception hierarchy for the Browser Engine.

Responsibilities:
    - Define browser-engine-specific exceptions.
    - Provide a common base exception for the Browser Engine.

Must NOT do:
    - Import Playwright.
    - Handle exceptions.
    - Contain browser logic.
"""


class BrowserEngineError(Exception):
    """
    Base exception for all Browser Engine errors.
    """

    pass


class BrowserLaunchError(BrowserEngineError):
    """
    Raised when the browser fails to launch.
    """

    pass


class BrowserClosedError(BrowserEngineError):
    """
    Raised when an operation is attempted on a closed browser.
    """

    pass


class SessionError(BrowserEngineError):
    """
    Raised when a browser session encounters an error.
    """

    pass


class PageError(BrowserEngineError):
    """
    Raised when a page operation fails.
    """

    pass


class LocatorError(BrowserEngineError):
    """
    Raised when a locator operation fails.
    """

    pass


class RecoverableError(BrowserEngineError):
    """
    Raised for errors that should be retried automatically (e.g. timeout, intermittent network).
    """
    pass


class FatalError(BrowserEngineError):
    """
    Raised for errors that cannot be recovered from by retrying (e.g. invalid credentials).
    """
    pass
