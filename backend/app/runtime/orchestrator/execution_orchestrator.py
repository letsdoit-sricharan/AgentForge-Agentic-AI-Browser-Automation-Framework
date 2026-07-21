"""
Execution Orchestrator

Public entry point for runtime execution.
Coordinates the entire execution lifecycle.

Responsibilities:
    - Accept OrchestratedRequest
    - Orchestrate plugin resolution
    - Orchestrate workflow resolution
    - Create WorkflowContext
    - Execute workflow through plugin
    - Return standardized OrchestratedResult
    - Handle execution failures consistently

Does NOT:
    - Know about specific plugins (BookMyShow, Amazon, etc.)
    - Know about specific workflows
    - Manage browser lifecycle directly
    - Import Playwright
    - Contain business logic
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.interfaces.plugin_context import PluginContext
from app.runtime.orchestrator.exceptions import (
    ExecutionPreparationError,
    OrchestrationPipelineError,
    PluginResolutionError,
    WorkflowContextCreationError,
    WorkflowResolutionError,
)
from app.runtime.orchestrator.execution_pipeline import (
    ExecutionPipeline,
    PipelineContext,
    PipelineStage,
)
from app.runtime.orchestrator.models import OrchestratedRequest, OrchestratedResult
from app.runtime.orchestrator.plugin_resolver import PluginResolver
from app.runtime.orchestrator.workflow_resolver import WorkflowResolver

if TYPE_CHECKING:
    from app.browser_engine.interfaces.page import Page
    from app.browser_engine.interfaces.session import Session
    from app.plugins.manager import PluginManager

logger = logging.getLogger(__name__)


class ExecutionOrchestrator:
    """
    Orchestrates execution from request to result.
    
    This is the primary entry point for executing plugins in AgentForge.
    It coordinates all the moving parts while remaining plugin-independent.
    """

    def __init__(
        self,
        plugin_manager: PluginManager,
    ) -> None:
        """
        Initialize the execution orchestrator.

        Args:
            plugin_manager: Plugin manager for plugin operations
        """
        self._plugin_manager = plugin_manager
        self._plugin_resolver = PluginResolver(plugin_manager.registry)
        self._workflow_resolver = WorkflowResolver()
        self._pipeline = ExecutionPipeline()
        self._logger = logger

        # Register pipeline stages
        self._setup_pipeline()

    def _setup_pipeline(self) -> None:
        """
        Configure the execution pipeline stages.
        """
        self._pipeline.register_stage(
            PipelineStage.PLUGIN_RESOLUTION,
            self._resolve_plugin_stage,
        )
        self._pipeline.register_stage(
            PipelineStage.WORKFLOW_RESOLUTION,
            self._resolve_workflow_stage,
        )

    async def execute(
        self,
        request: OrchestratedRequest,
        session: Session,
        page: Page,
        plugin_context: PluginContext,
    ) -> OrchestratedResult:
        """
        Execute an orchestrated request.

        Args:
            request: Execution request with plugin and workflow names
            session: Browser session for workflow
            page: Browser page for workflow
            plugin_context: Plugin context with framework services

        Returns:
            OrchestratedResult with execution outcome

        Raises:
            PluginResolutionError: If plugin cannot be resolved
            WorkflowResolutionError: If workflow cannot be resolved
            OrchestrationPipelineError: If execution fails
        """
        self._logger.info(
            f"Executing request {request.request_id}: "
            f"plugin={request.plugin_name}, workflow={request.workflow_name}"
        )

        started_at = datetime.utcnow()

        try:
            # Create pipeline context
            pipeline_context = PipelineContext(
                request=request,
            )

            # Execute pipeline stages
            pipeline_context = await self._pipeline.execute(pipeline_context)

            # Create workflow context
            workflow_context = self._create_workflow_context(
                request=request,
                plugin_context=plugin_context,
                session=session,
                page=page,
            )

            # Execute the workflow through the plugin
            workflow_result = await self._execute_workflow(
                plugin=pipeline_context.plugin,
                workflow=pipeline_context.workflow,
                workflow_context=workflow_context,
            )

            # Build success result
            completed_at = datetime.utcnow()
            execution_time = (completed_at - started_at).total_seconds()

            result = OrchestratedResult(
                request_id=request.request_id,
                plugin_name=request.plugin_name,
                workflow_name=request.workflow_name,
                success=True,
                output=self._extract_output(workflow_result),
                started_at=started_at,
                completed_at=completed_at,
                execution_time=execution_time,
                metadata={
                    "plugin_metadata": pipeline_context.plugin.metadata.__dict__,
                },
            )

            self._logger.info(
                f"Successfully executed request {request.request_id} "
                f"in {execution_time:.2f}s"
            )

            return result

        except (
            PluginResolutionError,
            WorkflowResolutionError,
            OrchestrationPipelineError,
        ) as e:
            # Expected orchestration errors
            completed_at = datetime.utcnow()
            execution_time = (completed_at - started_at).total_seconds()

            self._logger.error(
                f"Orchestration failed for request {request.request_id}: {e}"
            )

            return OrchestratedResult(
                request_id=request.request_id,
                plugin_name=request.plugin_name,
                workflow_name=request.workflow_name,
                success=False,
                errors=[str(e)],
                started_at=started_at,
                completed_at=completed_at,
                execution_time=execution_time,
            )

        except Exception as e:
            # Unexpected errors
            completed_at = datetime.utcnow()
            execution_time = (completed_at - started_at).total_seconds()

            self._logger.error(
                f"Unexpected error executing request {request.request_id}: {e}",
                exc_info=True,
            )

            return OrchestratedResult(
                request_id=request.request_id,
                plugin_name=request.plugin_name,
                workflow_name=request.workflow_name,
                success=False,
                errors=[f"Unexpected error: {str(e)}"],
                started_at=started_at,
                completed_at=completed_at,
                execution_time=execution_time,
            )

    async def _resolve_plugin_stage(
        self,
        context: PipelineContext,
    ) -> PipelineContext:
        """
        Pipeline stage: Resolve the plugin.

        Args:
            context: Pipeline context

        Returns:
            Updated context with plugin

        Raises:
            PluginResolutionError: If plugin cannot be resolved
        """
        request = context.request

        resolution = self._plugin_resolver.resolve(request.plugin_name)

        if not resolution.found or resolution.plugin is None:
            raise PluginResolutionError(
                request.plugin_name,
                resolution.error or "Plugin not found",
            )

        context.plugin = resolution.plugin
        return context

    async def _resolve_workflow_stage(
        self,
        context: PipelineContext,
    ) -> PipelineContext:
        """
        Pipeline stage: Resolve the workflow.

        Args:
            context: Pipeline context

        Returns:
            Updated context with workflow

        Raises:
            WorkflowResolutionError: If workflow cannot be resolved
        """
        request = context.request
        plugin = context.plugin

        resolution = self._workflow_resolver.resolve(
            plugin,
            request.workflow_name,
        )

        if not resolution.found or resolution.workflow is None:
            raise WorkflowResolutionError(
                request.workflow_name,
                request.plugin_name,
                resolution.error or "Workflow not found",
            )

        context.workflow = resolution.workflow
        return context

    def _create_workflow_context(
        self,
        request: OrchestratedRequest,
        plugin_context: PluginContext,
        session: Session,
        page: Page,
    ) -> WorkflowContext:
        """
        Create a WorkflowContext for workflow execution.

        Args:
            request: Orchestrated request
            plugin_context: Plugin context
            session: Browser session
            page: Browser page

        Returns:
            WorkflowContext instance

        Raises:
            WorkflowContextCreationError: If context creation fails
        """
        try:
            workflow_context = WorkflowContext(
                plugin_context=plugin_context,
                page=page,
                session=session,
                input_data=request.input_data,
                state={},
            )

            return workflow_context

        except Exception as e:
            raise WorkflowContextCreationError(str(e)) from e

    async def _execute_workflow(
        self,
        plugin: any,
        workflow: any,
        workflow_context: WorkflowContext,
    ):
        """
        Execute the workflow.

        Args:
            plugin: Plugin instance
            workflow: Workflow instance
            workflow_context: Workflow context

        Returns:
            Workflow execution result
        """
        # Execute through workflow's execute method
        result = await workflow.execute(workflow_context)
        return result

    def _extract_output(
        self,
        workflow_result,
    ) -> dict:
        """
        Extract output from workflow result.

        Args:
            workflow_result: Result from workflow execution

        Returns:
            Dictionary of output data
        """
        # Handle different result types
        if workflow_result is None:
            return {}

        if isinstance(workflow_result, dict):
            return workflow_result

        # Check if it's a dataclass or object with attributes
        if hasattr(workflow_result, "__dict__"):
            return workflow_result.__dict__

        # Wrap primitive types
        return {"result": workflow_result}

    def get_available_plugins(self) -> list[str]:
        """
        Get list of available plugin names.

        Returns:
            List of plugin names
        """
        return self._plugin_resolver.get_available_plugins()

    def get_plugin_capabilities(
        self,
        plugin_name: str,
    ) -> tuple[str, ...]:
        """
        Get capabilities of a plugin.

        Args:
            plugin_name: Name of the plugin

        Returns:
            Tuple of capability strings

        Raises:
            PluginResolutionError: If plugin not found
        """
        return self._plugin_resolver.get_plugin_capabilities(plugin_name)

    def find_plugins_by_capability(
        self,
        capability: str,
    ) -> list[str]:
        """
        Find plugins with a specific capability.

        Args:
            capability: Capability to search for

        Returns:
            List of plugin names
        """
        resolutions = self._plugin_resolver.resolve_by_capability(capability)
        return [r.plugin_name for r in resolutions]
