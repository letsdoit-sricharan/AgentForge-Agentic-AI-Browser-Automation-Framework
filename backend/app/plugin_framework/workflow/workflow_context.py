"""
Purpose:
    Defines the execution context for plugin workflows.

Responsibilities:
    - Provide controlled access to framework resources.
    - Store workflow input data.
    - Share execution state between workflow steps.
    - Own the active browser session/page for the lifetime of a workflow.

Does NOT:
    - Execute browser operations.
    - Import Playwright.
    - Contain website-specific logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.browser_engine.interfaces.page import Page
from app.browser_engine.interfaces.session import Session
from app.plugins.interfaces.plugin_context import PluginContext


@dataclass(slots=True)
class WorkflowContext:
    """
    Context passed to every workflow execution.
    """

    plugin_context: PluginContext

    page: Page

    session: Session

    input_data: dict[str, Any] = field(default_factory=dict)

    state: dict[str, Any] = field(default_factory=dict)