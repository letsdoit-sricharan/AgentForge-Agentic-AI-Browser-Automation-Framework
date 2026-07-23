"""
Orchestrator Models

Data structures used by the execution orchestrator.

These models are independent of plugins and browser implementations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4


@dataclass
class OrchestratedRequest:
    """
    Request for orchestrated execution.

    This is the high-level request that enters the orchestrator.
    It knows about plugin names and workflow names, but not implementations.
    """

    request_id: str = field(default_factory=lambda: str(uuid4()))
    plugin_name: str = ""
    workflow_name: str = ""
    input_data: dict[str, Any] = field(default_factory=dict)
    configuration: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class OrchestratedResult:
    """
    Result from orchestrated execution.

    Standardized result structure returned by the orchestrator.
    """

    request_id: str
    plugin_name: str
    workflow_name: str
    success: bool
    output: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    execution_time: float | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PluginResolution:
    """
    Result of plugin resolution.

    Contains the resolved plugin and validation information.
    """

    plugin_name: str
    found: bool
    plugin: Any = None  # Actual Plugin instance
    error: str | None = None
    capabilities: tuple[str, ...] = field(default_factory=tuple)


@dataclass
class WorkflowResolution:
    """
    Result of workflow resolution.

    Contains the resolved workflow and execution configuration.
    """

    workflow_name: str
    found: bool
    workflow: Any = None  # Actual Workflow instance
    error: str | None = None
    requires_context: bool = True
    configuration: dict[str, Any] = field(default_factory=dict)
