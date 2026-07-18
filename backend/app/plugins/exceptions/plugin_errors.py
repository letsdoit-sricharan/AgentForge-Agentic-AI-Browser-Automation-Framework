"""
Purpose:
    Defines the exception hierarchy for the Plugin Infrastructure.

Responsibilities:
    - Provide plugin-specific exceptions.
    - Allow precise error handling.
    - Improve debugging.

Does NOT:
    - Handle exceptions.
    - Recover from failures.
"""

from __future__ import annotations


class PluginError(Exception):
    """
    Base exception for all plugin-related errors.
    """


class PluginLoadError(PluginError):
    """
    Raised when a plugin cannot be loaded.
    """


class PluginRegistrationError(PluginError):
    """
    Raised when plugin registration fails.
    """


class PluginValidationError(PluginError):
    """
    Raised when a plugin fails validation.
    """


class PluginExecutionError(PluginError):
    """
    Raised when plugin execution fails.
    """