"""
Execution Pipeline

Orchestrates the execution stages in order.

Responsibilities:
    - Execute orchestration stages sequentially
    - Standardize error propagation
    - Track execution progress
    - Remain extensible for future middleware

Does NOT:
    - Know about specific plugins or workflows
    - Manage browser lifecycle
    - Import Playwright
    - Contain business logic
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Any, Callable

from app.runtime.orchestrator.exceptions import OrchestrationPipelineError

logger = logging.getLogger(__name__)


class PipelineStage(Enum):
    """
    Execution pipeline stages.
    """

    PLUGIN_RESOLUTION = auto()
    PLUGIN_INITIALIZATION = auto()
    WORKFLOW_RESOLUTION = auto()
    CONTEXT_CREATION = auto()
    WORKFLOW_EXECUTION = auto()
    RESULT_COLLECTION = auto()
    CLEANUP = auto()


@dataclass
class PipelineContext:
    """
    Context passed through pipeline stages.

    Accumulates data as it flows through the pipeline.
    """

    request: Any  # OrchestratedRequest
    plugin: Any = None
    workflow: Any = None
    workflow_context: Any = None
    result: Any = None
    errors: list[str] = None
    current_stage: PipelineStage | None = None
    started_at: datetime = None
    completed_at: datetime | None = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.started_at is None:
            self.started_at = datetime.utcnow()


class ExecutionPipeline:
    """
    Orchestrates execution through defined stages.

    Implements a flexible pipeline pattern that can be extended
    with middleware, hooks, and custom stages.
    """

    def __init__(self) -> None:
        """
        Initialize the execution pipeline.
        """
        self._logger = logger
        self._stages: list[tuple[PipelineStage, Callable]] = []
        self._middleware: list[Callable] = []

    def register_stage(
        self,
        stage: PipelineStage,
        handler: Callable,
    ) -> None:
        """
        Register a pipeline stage handler.

        Args:
            stage: Pipeline stage
            handler: Callable that processes the stage
        """
        self._stages.append((stage, handler))
        self._logger.debug(f"Registered stage: {stage.name}")

    def register_middleware(
        self,
        middleware: Callable,
    ) -> None:
        """
        Register middleware that runs before each stage.

        Args:
            middleware: Callable that processes the context
        """
        self._middleware.append(middleware)
        self._logger.debug(f"Registered middleware: {middleware.__name__}")

    async def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext:
        """
        Execute the pipeline stages.

        Args:
            context: Pipeline context to process

        Returns:
            Updated pipeline context

        Raises:
            OrchestrationPipelineError: If any stage fails
        """
        self._logger.info("Starting pipeline execution")

        try:
            # Execute each stage in order
            for stage, handler in self._stages:
                context.current_stage = stage
                self._logger.debug(f"Executing stage: {stage.name}")

                # Run middleware
                for middleware in self._middleware:
                    try:
                        context = await self._run_async_or_sync(middleware, context)
                    except Exception as e:
                        self._logger.warning(
                            f"Middleware {middleware.__name__} failed: {e}"
                        )

                # Run stage handler
                try:
                    context = await self._run_async_or_sync(handler, context)
                except Exception as e:
                    error_msg = f"Stage {stage.name} failed: {str(e)}"
                    self._logger.error(error_msg, exc_info=True)
                    context.errors.append(error_msg)
                    raise OrchestrationPipelineError(stage.name, str(e)) from e

            # Mark completion
            context.completed_at = datetime.utcnow()
            self._logger.info("Pipeline execution completed successfully")

            return context

        except Exception as e:
            context.completed_at = datetime.utcnow()
            if not isinstance(e, OrchestrationPipelineError):
                # Wrap unexpected errors
                stage_name = context.current_stage.name if context.current_stage else "Unknown"
                raise OrchestrationPipelineError(stage_name, str(e)) from e
            raise

    async def _run_async_or_sync(
        self,
        func: Callable,
        context: PipelineContext,
    ) -> PipelineContext:
        """
        Run a function that may be async or sync.

        Args:
            func: Function to run
            context: Pipeline context

        Returns:
            Updated context
        """
        import inspect

        if inspect.iscoroutinefunction(func):
            result = await func(context)
        else:
            result = func(context)

        # If handler returns None, return original context
        return result if result is not None else context

    def clear_stages(self) -> None:
        """
        Clear all registered stages.

        Useful for testing or reconfiguration.
        """
        self._stages.clear()
        self._logger.debug("Cleared all pipeline stages")

    def clear_middleware(self) -> None:
        """
        Clear all registered middleware.

        Useful for testing or reconfiguration.
        """
        self._middleware.clear()
        self._logger.debug("Cleared all middleware")

    def get_stages(self) -> list[PipelineStage]:
        """
        Get list of registered stages.

        Returns:
            List of pipeline stages
        """
        return [stage for stage, _ in self._stages]

    def has_stage(
        self,
        stage: PipelineStage,
    ) -> bool:
        """
        Check if a stage is registered.

        Args:
            stage: Pipeline stage to check

        Returns:
            True if stage is registered
        """
        return any(s == stage for s, _ in self._stages)
