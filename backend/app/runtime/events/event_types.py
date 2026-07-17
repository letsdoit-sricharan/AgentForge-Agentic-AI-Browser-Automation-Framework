"""
Event type definitions.

Defines all event types emitted by the Agent Runtime.

This module contains only strongly typed enums and
does not implement any runtime logic.
"""

from __future__ import annotations

from enum import Enum


class EventCategory(str, Enum):
    """
    High-level event categories.
    """

    RUNTIME = "runtime"
    BROWSER = "browser"
    WORKFLOW = "workflow"


class RuntimeEventType(str, Enum):
    """
    Runtime lifecycle events.
    """

    STARTED = "runtime.started"
    PAUSED = "runtime.paused"
    RESUMED = "runtime.resumed"
    STOPPED = "runtime.stopped"
    COMPLETED = "runtime.completed"
    FAILED = "runtime.failed"


class BrowserEventType(str, Enum):
    """
    Browser execution events.
    """

    BROWSER_STARTED = "browser.started"
    BROWSER_CLOSED = "browser.closed"

    SESSION_CREATED = "browser.session.created"
    SESSION_CLOSED = "browser.session.closed"

    PAGE_CREATED = "browser.page.created"
    PAGE_CLOSED = "browser.page.closed"

    NAVIGATION_STARTED = "browser.navigation.started"
    NAVIGATION_COMPLETED = "browser.navigation.completed"

    ELEMENT_FOUND = "browser.element.found"
    ELEMENT_NOT_FOUND = "browser.element.not_found"

    SCREENSHOT_CAPTURED = "browser.screenshot.captured"


class WorkflowEventType(str, Enum):
    """
    Workflow execution events.
    """

    WORKFLOW_STARTED = "workflow.started"
    WORKFLOW_COMPLETED = "workflow.completed"
    WORKFLOW_FAILED = "workflow.failed"

    TASK_STARTED = "workflow.task.started"
    TASK_COMPLETED = "workflow.task.completed"
    TASK_FAILED = "workflow.task.failed"

    CHECKPOINT_CREATED = "workflow.checkpoint.created"
    CHECKPOINT_RESTORED = "workflow.checkpoint.restored"