"""
Tests for TaskExecutor

Tests cover:
    - Task execution flow
    - Plugin resolution
    - Task validation
    - Error handling
    - Result conversion
"""

from dataclasses import dataclass
from typing import Any
from unittest.mock import AsyncMock, Mock

import pytest

from app.runtime.orchestrator.models import OrchestratedResult
from app.runtime.tasks.task import Task
from app.runtime.tasks.task_executor import TaskExecutor
from app.runtime.tasks.task_registry import TaskRegistry
from app.runtime.tasks.task_result import TaskStatus


# Test task implementation
@dataclass
class TestTask(Task):
    """Test task implementation."""

    name: str
    should_fail_validation: bool = False

    @property
    def task_type(self) -> str:
        return "test_task"

    def validate(self) -> tuple[bool, list[str]]:
        if self.should_fail_validation:
            return (False, ["Validation failed"])

        errors = []
        if not self.name:
            errors.append("Name is required")

        return (len(errors) == 0, errors)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_type": self.task_type,
            "name": self.name,
        }


@pytest.fixture
def task_registry():
    """Create a TaskRegistry for testing."""
    return TaskRegistry()


@pytest.fixture
def mock_orchestrator():
    """Create a mock ExecutionOrchestrator."""
    return Mock()


@pytest.fixture
def task_executor(mock_orchestrator, task_registry):
    """Create a TaskExecutor for testing."""
    return TaskExecutor(mock_orchestrator, task_registry)


@pytest.fixture
def mock_session():
    """Create a mock Session."""
    return Mock()


@pytest.fixture
def mock_page():
    """Create a mock Page."""
    return Mock()


@pytest.fixture
def mock_plugin_context():
    """Create a mock PluginContext."""
    return Mock()


class TestTaskExecutorInitialization:
    """Test TaskExecutor initialization."""

    def test_initialize(self, mock_orchestrator, task_registry):
        """Test creating TaskExecutor."""
        executor = TaskExecutor(mock_orchestrator, task_registry)

        assert executor._orchestrator == mock_orchestrator
        assert executor._registry == task_registry


class TestTaskExecution:
    """Test task execution."""

    @pytest.mark.asyncio
    async def test_execute_valid_task(
        self,
        task_executor,
        task_registry,
        mock_orchestrator,
        mock_session,
        mock_page,
        mock_plugin_context,
    ):
        """Test executing a valid task."""
        # Setup
        task_registry.register_task("test_task", "test_plugin")
        task = TestTask(name="test")

        # Mock orchestrator response
        orchestrated_result = OrchestratedResult(
            request_id=task.task_id,
            plugin_name='test_plugin',
            workflow_name='test_task_workflow',
            success=True,
            output={"result": "success"},
            errors=[],
            execution_time=1.5,
        )
        mock_orchestrator.execute = AsyncMock(return_value=orchestrated_result)

        # Execute
        result = await task_executor.execute_task(
            task=task,
            session=mock_session,
            page=mock_page,
            plugin_context=mock_plugin_context,
        )

        # Verify
        assert result.success
        assert result.status == TaskStatus.COMPLETED
        assert result.task_id == task.task_id
        assert result.task_type == "test_task"
        assert result.output == {"result": "success"}
        assert result.plugin_name == "test_plugin"
        assert result.workflow_name == "test_task_workflow"

    @pytest.mark.asyncio
    async def test_execute_task_validation_failure(
        self,
        task_executor,
        task_registry,
        mock_session,
        mock_page,
        mock_plugin_context,
    ):
        """Test executing task with validation failure."""
        # Setup
        task_registry.register_task("test_task", "test_plugin")
        task = TestTask(name="test", should_fail_validation=True)

        # Execute
        result = await task_executor.execute_task(
            task=task,
            session=mock_session,
            page=mock_page,
            plugin_context=mock_plugin_context,
        )

        # Verify
        assert not result.success
        assert result.status == TaskStatus.FAILED
        assert "Validation failed" in result.errors

    @pytest.mark.asyncio
    async def test_execute_task_not_supported(
        self,
        task_executor,
        mock_session,
        mock_page,
        mock_plugin_context,
    ):
        """Test executing unsupported task type."""
        # Setup
        task = TestTask(name="test")
        # Do NOT register the task type

        # Execute
        result = await task_executor.execute_task(
            task=task,
            session=mock_session,
            page=mock_page,
            plugin_context=mock_plugin_context,
        )

        # Verify
        assert not result.success
        assert result.status == TaskStatus.FAILED
        assert len(result.errors) > 0

    @pytest.mark.asyncio
    async def test_execute_task_orchestrator_failure(
        self,
        task_executor,
        task_registry,
        mock_orchestrator,
        mock_session,
        mock_page,
        mock_plugin_context,
    ):
        """Test executing task when orchestrator fails."""
        # Setup
        task_registry.register_task("test_task", "test_plugin")
        task = TestTask(name="test")

        # Mock orchestrator failure
        orchestrated_result = OrchestratedResult(
            request_id=task.task_id,
            plugin_name='test_plugin',
            workflow_name='test_task_workflow',
            success=False,
            output={},
            errors=["Orchestration failed"],
            execution_time=0.5,
        )
        mock_orchestrator.execute = AsyncMock(return_value=orchestrated_result)

        # Execute
        result = await task_executor.execute_task(
            task=task,
            session=mock_session,
            page=mock_page,
            plugin_context=mock_plugin_context,
        )

        # Verify
        assert not result.success
        assert result.status == TaskStatus.FAILED
        assert "Orchestration failed" in result.errors


class TestPluginResolution:
    """Test plugin and workflow resolution."""

    @pytest.mark.asyncio
    async def test_resolves_correct_plugin(
        self,
        task_executor,
        task_registry,
        mock_orchestrator,
        mock_session,
        mock_page,
        mock_plugin_context,
    ):
        """Test that correct plugin is resolved."""
        # Setup
        task_registry.register_task("test_task", "test_plugin")
        task = TestTask(name="test")

        # Mock orchestrator
        orchestrated_result = OrchestratedResult(
            request_id=task.task_id,
            plugin_name='test_plugin',
            workflow_name='test_task_workflow',
            success=True,
            output={},
            errors=[],
            execution_time=1.0,
        )
        mock_orchestrator.execute = AsyncMock(return_value=orchestrated_result)

        # Execute
        result = await task_executor.execute_task(
            task=task,
            session=mock_session,
            page=mock_page,
            plugin_context=mock_plugin_context,
        )

        # Verify correct plugin was used
        assert result.plugin_name == "test_plugin"

    @pytest.mark.asyncio
    async def test_resolves_workflow_name(
        self,
        task_executor,
        task_registry,
        mock_orchestrator,
        mock_session,
        mock_page,
        mock_plugin_context,
    ):
        """Test that workflow name is correctly derived."""
        # Setup
        task_registry.register_task("test_task", "test_plugin")
        task = TestTask(name="test")

        # Mock orchestrator
        orchestrated_result = OrchestratedResult(
            request_id=task.task_id,
            plugin_name='test_plugin',
            workflow_name='test_task_workflow',
            success=True,
            output={},
            errors=[],
            execution_time=1.0,
        )
        mock_orchestrator.execute = AsyncMock(return_value=orchestrated_result)

        # Execute
        result = await task_executor.execute_task(
            task=task,
            session=mock_session,
            page=mock_page,
            plugin_context=mock_plugin_context,
        )

        # Verify workflow name (convention: {task_type}_workflow)
        assert result.workflow_name == "test_task_workflow"

    @pytest.mark.asyncio
    async def test_uses_first_plugin_when_multiple(
        self,
        task_executor,
        task_registry,
        mock_orchestrator,
        mock_session,
        mock_page,
        mock_plugin_context,
    ):
        """Test that first plugin is used when multiple support task."""
        # Setup - register multiple plugins
        task_registry.register_task("test_task", "plugin1")
        task_registry.register_task("test_task", "plugin2")
        task_registry.register_task("test_task", "plugin3")

        task = TestTask(name="test")

        # Mock orchestrator
        orchestrated_result = OrchestratedResult(
            request_id=task.task_id,
            plugin_name='test_plugin',
            workflow_name='test_task_workflow',
            success=True,
            output={},
            errors=[],
            execution_time=1.0,
        )
        mock_orchestrator.execute = AsyncMock(return_value=orchestrated_result)

        # Execute
        result = await task_executor.execute_task(
            task=task,
            session=mock_session,
            page=mock_page,
            plugin_context=mock_plugin_context,
        )

        # Verify first plugin was used
        assert result.plugin_name == "plugin1"


class TestTaskExecutorQueries:
    """Test executor query methods."""

    def test_can_execute_task(self, task_executor, task_registry):
        """Test checking if task can be executed."""
        task_registry.register_task("test_task", "test_plugin")

        assert task_executor.can_execute_task("test_task")
        assert not task_executor.can_execute_task("unknown_task")

    def test_get_supported_task_types(self, task_executor, task_registry):
        """Test getting supported task types."""
        task_registry.register_task("task1", "plugin1")
        task_registry.register_task("task2", "plugin2")

        types = task_executor.get_supported_task_types()

        assert len(types) == 2
        assert "task1" in types
        assert "task2" in types


class TestTaskResultConversion:
    """Test conversion of OrchestratedResult to TaskResult."""

    @pytest.mark.asyncio
    async def test_converts_successful_result(
        self,
        task_executor,
        task_registry,
        mock_orchestrator,
        mock_session,
        mock_page,
        mock_plugin_context,
    ):
        """Test converting successful orchestrated result."""
        # Setup
        task_registry.register_task("test_task", "test_plugin")
        task = TestTask(name="test")

        output = {"data": "result", "count": 42}
        orchestrated_result = OrchestratedResult(
            request_id=task.task_id,
            plugin_name='test_plugin',
            workflow_name='test_task_workflow',
            success=True,
            output=output,
            errors=[],
            execution_time=2.5,
        )
        mock_orchestrator.execute = AsyncMock(return_value=orchestrated_result)

        # Execute
        result = await task_executor.execute_task(
            task=task,
            session=mock_session,
            page=mock_page,
            plugin_context=mock_plugin_context,
        )

        # Verify
        assert result.status == TaskStatus.COMPLETED
        assert result.output == output
        assert result.errors == []
        assert "execution_time" in result.metadata

    @pytest.mark.asyncio
    async def test_converts_failed_result(
        self,
        task_executor,
        task_registry,
        mock_orchestrator,
        mock_session,
        mock_page,
        mock_plugin_context,
    ):
        """Test converting failed orchestrated result."""
        # Setup
        task_registry.register_task("test_task", "test_plugin")
        task = TestTask(name="test")

        errors = ["Error 1", "Error 2"]
        orchestrated_result = OrchestratedResult(
            request_id=task.task_id,
            plugin_name='test_plugin',
            workflow_name='test_task_workflow',
            success=False,
            output={},
            errors=errors,
            execution_time=1.0,
        )
        mock_orchestrator.execute = AsyncMock(return_value=orchestrated_result)

        # Execute
        result = await task_executor.execute_task(
            task=task,
            session=mock_session,
            page=mock_page,
            plugin_context=mock_plugin_context,
        )

        # Verify
        assert result.status == TaskStatus.FAILED
        assert result.errors == errors


class TestTaskContextCreation:
    """Test TaskContext creation."""

    @pytest.mark.asyncio
    async def test_creates_task_context(
        self,
        task_executor,
        task_registry,
        mock_orchestrator,
        mock_session,
        mock_page,
        mock_plugin_context,
    ):
        """Test that TaskContext is created from Task."""
        # Setup
        task_registry.register_task("test_task", "test_plugin")
        task = TestTask(
            name="test",
            priority=5,
            correlation_id="corr-123",
            metadata={"key": "value"},
        )

        orchestrated_result = OrchestratedResult(
            request_id=task.task_id,
            plugin_name='test_plugin',
            workflow_name='test_task_workflow',
            success=True,
            output={},
            errors=[],
            execution_time=1.0,
        )
        mock_orchestrator.execute = AsyncMock(return_value=orchestrated_result)

        # Execute
        await task_executor.execute_task(
            task=task,
            session=mock_session,
            page=mock_page,
            plugin_context=mock_plugin_context,
        )

        # TaskContext is created internally and passed to orchestrator
        # We verify this indirectly through successful execution
        assert mock_orchestrator.execute.called
