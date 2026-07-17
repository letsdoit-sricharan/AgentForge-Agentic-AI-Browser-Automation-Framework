"""
Exceptions for the Action Library.
"""

from __future__ import annotations


class ActionError(Exception):
    """
    Base exception for all Action Library errors.
    """


class ActionExecutionError(ActionError):
    """
    Raised when an action fails during execution.
    """


class ActionTimeoutError(ActionExecutionError):
    """
    Raised when an action exceeds its timeout.
    """


class InvalidActionError(ActionError):
    """
    Raised when an action is configured incorrectly.
    """


class ElementNotFoundError(ActionExecutionError):
    """
    Raised when the target element cannot be located.
    """


class ElementNotInteractableError(ActionExecutionError):
    """
    Raised when an element exists but cannot be interacted with.
    """