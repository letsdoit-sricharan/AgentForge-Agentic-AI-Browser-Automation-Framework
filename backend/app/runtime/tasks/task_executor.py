"""
Task Executor

Executes tasks by resolving plugins and delegating to the Execution Orchestrator.

Responsibilities:
    - Accept generic Tasks
    - Resolve which plugin can execute them
    - Convert Task → OrchestratedRequest
    - Delegate to Execution Orchestrator
    - Convert OrchestratedResult → TaskResult

Does NOT:
    - Know about specific task types
    - Execute browser operations
    - Import Playwright
    - Contain business logic
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING

from app.runtime.orchestrator.models import OrchestratedRequest
from app.runtime.tasks.exceptions import (
    TaskExecutionError,
    TaskNotSupportedError,
    TaskResolutionError,
)
from app.runtime.tasks.task import Task
from app.runtime.tasks.task_context import TaskContext
from app.runtime.tasks.task_registry import TaskRegistry
from app.runtime.tasks.task_result import TaskResult, TaskStatus

if TYPE_CHECKING:
    from app.browser_engine.interfaces.page import Page
    from app.browser_engine.interfaces.session import Session
    from app.plugins.interfaces.plugin_context import PluginContext
    from app.runtime.orchestrator.execution_orchestrator import ExecutionOrchestrator

logger = logging.getLogger(__name__)


class TaskExecutor:
    """
    Executes tasks by delegating to the appropriate plugin via the orchestrator.
    
    This is the bridge between the task abstraction layer and the execution layer.
    
    Flow:
        Task → TaskExecutor → Orchestrator → Plugin → Workflow → Result
    """

    def __init__(
        self,
        orchestrator: ExecutionOrchestrator,
        task_registry: TaskRegistry,
    ) -> None:
        """
        Initialize the task executor.
        
        Args:
            orchestrator: Execution orchestrator for plugin execution
            task_registry: Task registry for plugin resolution
        """
        self._orchestrator = orchestrator
        self._registry = task_registry
        self._logger = logger

    async def execute_task(
        self,
        task: Task,
        session: Session,
        page: Page,
        plugin_context: PluginContext,
        task_context: TaskContext | None = None,
    ) -> TaskResult:
        """
        Execute a task.
        
        Args:
            task: Task to execute
            session: Browser session
            page: Browser page
            plugin_context: Plugin context
            task_context: Optional task context (created if not provided)
            
        Returns:
            TaskResult with execution outcome
            
        Raises:
            TaskNotSupportedError: If no plugin supports the task
            TaskResolutionError: If plugin/workflow resolution fails
            TaskExecutionError: If execution fails
        """
        started_at = datetime.utcnow()
        
        # Create task context if not provided
        if task_context is None:
            task_context = self._create_task_context(task)
        
        self._logger.info(
            f"Executing task: {task.task_type} (ID: {task.task_id})"
        )
        
        try:
            # Validate task
            is_valid, errors = task.validate()
            if not is_valid:
                return self._create_error_result(
                    task,
                    TaskStatus.FAILED,
                    errors,
                    started_at,
                )
            
            # Resolve which plugin can execute this task
            plugin_name, workflow_name = self._resolve_plugin_and_workflow(
                task.task_type
            )
            
            # Convert Task → OrchestratedRequest
            orchestrated_request = self._task_to_orchestrated_request(
                task,
                plugin_name,
                workflow_name,
            )
            
            # Execute via orchestrator
            orchestrated_result = await self._orchestrator.execute(
                request=orchestrated_request,
                session=session,
                page=page,
                plugin_context=plugin_context,
            )
            
            # Convert OrchestratedResult → TaskResult
            task_result = self._orchestrated_result_to_task_result(
                task,
                orchestrated_result,
                plugin_name,
                workflow_name,
                started_at,
            )
            
            self._logger.info(
                f"Task {task.task_id} completed with status: {task_result.status.name}"
            )
            
            return task_result
            
        except TaskNotSupportedError as e:
            self._logger.error(f"Task not supported: {e}")
            return self._create_error_result(
                task,
                TaskStatus.FAILED,
                [str(e)],
                started_at,
            )
        
        except TaskResolutionError as e:
            self._logger.error(f"Task resolution failed: {e}")
            return self._create_error_result(
                task,
                TaskStatus.FAILED,
                [str(e)],
                started_at,
            )
        
        except Exception as e:
            self._logger.error(
                f"Task execution failed: {e}",
                exc_info=True,
            )
            return self._create_error_result(
                task,
                TaskStatus.FAILED,
                [f"Unexpected error: {str(e)}"],
                started_at,
            )

    def _create_task_context(
        self,
        task: Task,
    ) -> TaskContext:
        """
        Create TaskContext from Task.
        
        Args:
            task: Task instance
            
        Returns:
            TaskContext
        """
        return TaskContext(
            task_id=task.task_id,
            task_type=task.task_type,
            input_data=task.to_dict(),
            priority=task.priority,
            correlation_id=task.correlation_id,
            metadata=task.metadata,
        )

    def _resolve_plugin_and_workflow(
        self,
        task_type: str,
    ) -> tuple[str, str]:
        """
        Resolve which plugin and workflow can execute a task type.
        
        Args:
            task_type: Task type identifier
            
        Returns:
            Tuple of (plugin_name, workflow_name)
            
        Raises:
            TaskNotSupportedError: If no plugin supports the task
            TaskResolutionError: If resolution fails
        """
        # Get plugins that support this task type
        try:
            supporting_plugins = self._registry.get_supporting_plugins(task_type)
        except TaskNotSupportedError:
            raise
        
        if not supporting_plugins:
            raise TaskNotSupportedError(
                task_type,
                "No plugins registered for this task type",
            )
        
        # Use the first supporting plugin
        # TODO: In future, add plugin selection strategy (priority, load balancing, etc.)
        plugin_name = supporting_plugins[0]
        
        # Derive workflow name from task type
        # Convention: task_type "search_movie" → workflow "search_movie_workflow"
        workflow_name = f"{task_type}_workflow"
        
        self._logger.debug(
            f"Resolved task '{task_type}' to plugin '{plugin_name}', "
            f"workflow '{workflow_name}'"
        )
        
        return plugin_name, workflow_name

    def _task_to_orchestrated_request(
        self,
        task: Task,
        plugin_name: str,
        workflow_name: str,
    ) -> OrchestratedRequest:
        """
        Convert Task to OrchestratedRequest.
        
        Args:
            task: Task instance
            plugin_name: Target plugin name
            workflow_name: Target workflow name
            
        Returns:
            OrchestratedRequest
        """
        return OrchestratedRequest(
            request_id=task.task_id,
            plugin_name=plugin_name,
            workflow_name=workflow_name,
            input_data=task.to_dict(),
            configuration={},
            metadata={
                "task_type": task.task_type,
                "task_id": task.task_id,
                "priority": task.priority,
                "correlation_id": task.correlation_id,
            },
        )

    def _orchestrated_result_to_task_result(
        self,
        task: Task,
        orchestrated_result,
        plugin_name: str,
        workflow_name: str,
        started_at: datetime,
    ) -> TaskResult:
        """
        Convert OrchestratedResult to TaskResult.
        
        Args:
            task: Original task
            orchestrated_result: Result from orchestrator
            plugin_name: Plugin that executed the task
            workflow_name: Workflow that executed the task
            started_at: Execution start time
            
        Returns:
            TaskResult
        """
        status = TaskStatus.COMPLETED if orchestrated_result.success else TaskStatus.FAILED
        
        return TaskResult(
            task_id=task.task_id,
            task_type=task.task_type,
            status=status,
            started_at=started_at,
            completed_at=datetime.utcnow(),
            output=orchestrated_result.output,
            errors=orchestrated_result.errors,
            plugin_name=plugin_name,
            workflow_name=workflow_name,
            metadata={
                "orchestrated_result_id": orchestrated_result.request_id,
                "execution_time": orchestrated_result.execution_time,
            },
        )

    def _create_error_result(
        self,
        task: Task,
        status: TaskStatus,
        errors: list[str],
        started_at: datetime,
    ) -> TaskResult:
        """
        Create an error TaskResult.
        
        Args:
            task: Task that failed
            status: Task status
            errors: Error messages
            started_at: Execution start time
            
        Returns:
            TaskResult with error information
        """
        return TaskResult(
            task_id=task.task_id,
            task_type=task.task_type,
            status=status,
            started_at=started_at,
            completed_at=datetime.utcnow(),
            errors=errors,
        )

    def can_execute_task(
        self,
        task_type: str,
    ) -> bool:
        """
        Check if a task type can be executed.
        
        Args:
            task_type: Task type identifier
            
        Returns:
            True if at least one plugin supports the task
        """
        return self._registry.is_task_supported(task_type)

    def get_supported_task_types(self) -> list[str]:
        """
        Get all supported task types.
        
        Returns:
            List of task type identifiers
        """
        return self._registry.get_all_task_types()
