"""
Tests for ExecutionOrchestrator.
"""

import pytest

from app.plugins import PluginManager, PluginRegistry
from app.plugins.interfaces import Plugin, PluginContext, PluginMetadata
from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.runtime.orchestrator.execution_orchestrator import ExecutionOrchestrator
from app.runtime.orchestrator.models import OrchestratedRequest


class DummyWorkflow:
    """Mock workflow for testing."""

    async def execute(self, context: WorkflowContext):
        return {"status": "success", "result": "completed"}


class DummyPlugin(Plugin):
    """Mock plugin for testing."""

    def __init__(self, name: str = "test_plugin"):
        self._metadata = PluginMetadata(
            name=name,
            version="1.0.0",
            description="Test plugin",
            author="Test",
            capabilities=("testing",),
        )
        self._workflow = DummyWorkflow()
        self.workflows = {
            "test_workflow": self._workflow,
        }

    @property
    def metadata(self):
        return self._metadata

    def initialize(self, context: PluginContext) -> None:
        pass

    async def execute(self, context: WorkflowContext):
        return await self._workflow.execute(context)

    def shutdown(self) -> None:
        pass


class TestExecutionOrchestrator:
    """Tests for ExecutionOrchestrator."""

    @pytest.fixture
    def plugin_manager(self):
        """Create a plugin manager with test plugin."""
        registry = PluginRegistry()
        plugin = DummyPlugin("test_plugin")
        registry.register(plugin)
        
        # Mock plugin manager
        manager = type("PluginManager", (), {
            "registry": registry,
            "get_plugin": lambda self, name: registry.get(name),
        })()
        
        return manager

    @pytest.fixture
    def orchestrator(self, plugin_manager):
        """Create an execution orchestrator."""
        return ExecutionOrchestrator(plugin_manager)

    @pytest.fixture
    def request(self):
        """Create an orchestrated request."""
        return OrchestratedRequest(
            plugin_name="test_plugin",
            workflow_name="test_workflow",
            input_data={"key": "value"},
        )

    @pytest.fixture
    def mock_session(self):
        """Create a mock session."""
        return type("Session", (), {})()

    @pytest.fixture
    def mock_page(self):
        """Create a mock page."""
        return type("Page", (), {})()

    @pytest.fixture
    def plugin_context(self):
        """Create a plugin context."""
        return PluginContext(
            runtime=None,
            actions=None,
            memory=None,
            configuration=None,
            logger=None,
        )

    @pytest.mark.asyncio
    async def test_execute_success(
        self, orchestrator, request, mock_session, mock_page, plugin_context
    ):
        """Test successful execution."""
        result = await orchestrator.execute(
            request=request,
            session=mock_session,
            page=mock_page,
            plugin_context=plugin_context,
        )

        assert result.success is True
        assert result.request_id == request.request_id
        assert result.plugin_name == "test_plugin"
        assert result.workflow_name == "test_workflow"
        assert result.errors == []
        assert result.execution_time is not None
        assert result.execution_time > 0

    @pytest.mark.asyncio
    async def test_execute_plugin_not_found(
        self, orchestrator, mock_session, mock_page, plugin_context
    ):
        """Test execution with non-existent plugin."""
        request = OrchestratedRequest(
            plugin_name="nonexistent",
            workflow_name="test_workflow",
        )

        result = await orchestrator.execute(
            request=request,
            session=mock_session,
            page=mock_page,
            plugin_context=plugin_context,
        )

        assert result.success is False
        assert len(result.errors) > 0
        assert "not found" in result.errors[0].lower()

    @pytest.mark.asyncio
    async def test_execute_workflow_not_found(
        self, orchestrator, mock_session, mock_page, plugin_context
    ):
        """Test execution with non-existent workflow."""
        request = OrchestratedRequest(
            plugin_name="test_plugin",
            workflow_name="nonexistent_workflow",
        )

        result = await orchestrator.execute(
            request=request,
            session=mock_session,
            page=mock_page,
            plugin_context=plugin_context,
        )

        assert result.success is False
        assert len(result.errors) > 0

    def test_get_available_plugins(self, orchestrator):
        """Test getting available plugins."""
        plugins = orchestrator.get_available_plugins()

        assert "test_plugin" in plugins

    def test_get_plugin_capabilities(self, orchestrator):
        """Test getting plugin capabilities."""
        capabilities = orchestrator.get_plugin_capabilities("test_plugin")

        assert "testing" in capabilities

    def test_find_plugins_by_capability(self, orchestrator):
        """Test finding plugins by capability."""
        plugins = orchestrator.find_plugins_by_capability("testing")

        assert "test_plugin" in plugins
