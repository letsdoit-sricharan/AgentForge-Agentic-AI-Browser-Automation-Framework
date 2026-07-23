"""
Purpose:
    Defines exceptions for the Plugin Framework.

Responsibilities:
    - Represent workflow-related failures.
    - Provide a reusable exception hierarchy.

Does NOT:
    - Handle browser errors.
    - Handle runtime execution errors.
    - Import Playwright.
"""

from __future__ import annotations


class WorkflowError(Exception):
    """
    Base exception for all workflow-related errors.
    """


class WorkflowExecutionError(WorkflowError):
    """
    Raised when a workflow fails during execution.
    """


class StepExecutionError(WorkflowError):
    """
    Raised when a workflow step fails.
    """


class ValidationError(WorkflowError):
    """
    Raised when workflow validation fails.
    """


class WorkflowConfigurationError(WorkflowError):
    """
    Raised when a workflow is incorrectly configured.
    """
