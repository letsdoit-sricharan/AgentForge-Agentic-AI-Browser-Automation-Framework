"""
Execution Orchestrator

The orchestration layer that sits between Runtime and Plugin Framework.
Coordinates plugin resolution, workflow execution, and result handling.

Architecture:
    ExecutionOrchestrator - Public entry point for execution
    PluginResolver - Determines which plugin to use
    WorkflowResolver - Resolves workflow within plugin
    ExecutionPipeline - Orchestrates execution stages

Key Principles:
    - Plugin-independent: No knowledge of specific plugins
    - Browser-independent: No Playwright dependencies
    - Clean Architecture: Clear separation of concerns
    - SOLID: Single responsibility per component
"""

from app.runtime.orchestrator.execution_orchestrator import ExecutionOrchestrator
from app.runtime.orchestrator.execution_pipeline import ExecutionPipeline
from app.runtime.orchestrator.plugin_resolver import PluginResolver
from app.runtime.orchestrator.workflow_resolver import WorkflowResolver

__all__ = [
    "ExecutionOrchestrator",
    "ExecutionPipeline",
    "PluginResolver",
    "WorkflowResolver",
]
