"""
Purpose:
    Defines the execution context for plugin workflows.

Responsibilities:
    - Provide controlled access to framework resources.
    - Store workflow input data.
    - Share execution state between workflow steps.

Does NOT:
    - Execute browser operations.
    - Import Playwright.
    - Contain website-specific logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.plugins.interfaces import PluginContext


@dataclass(slots=True)
class WorkflowContext:
    """
    Context passed to every workflow execution.
    """

    plugin_context: PluginContext

    input_data: dict[str, Any] = field(default_factory=dict)

    state: dict[str, Any] = field(default_factory=dict)