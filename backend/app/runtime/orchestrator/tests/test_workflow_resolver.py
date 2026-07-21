"""
Tests for WorkflowResolver.
"""

import pytest

from app.runtime.orchestrator.workflow_resolver import WorkflowResolver


class DummyWorkflow:
    """Mock workflow for testing."""

    async def execute(self, context):
        return {"status": "success"}


class InvalidWorkflow:
    """Mock workflow without execute method."""

    pass


class DummyPlugin:
    """Mock plugin with workflows."""

    def __init__(self):
        self.metadata = type("Metadata", (), {"name": "test_plugin"})()
        self._workflow = DummyWorkflow()
        self.workflows = {
            "booking_workflow": DummyWorkflow(),
            "search_workflow": DummyWorkflow(),
        }


class TestWorkflowResolver:
    """Tests for WorkflowResolver."""

    @pytest.fixture
    def resolver(self):
        """Create a workflow resolver."""
        return WorkflowResolver()

    @pytest.fixture
    def plugin(self):
        """Create a test plugin."""
        return DummyPlugin()

    def test_resolve_workflow_from_dict(self, resolver, plugin):
        """Test resolving workflow from workflows dict."""
        resolution = resolver.resolve(plugin, "booking_workflow")

        assert resolution.found is True
        assert resolution.workflow is not None
        assert resolution.error is None

    def test_resolve_workflow_from_attribute(self, resolver, plugin):
        """Test resolving workflow from direct attribute."""
        resolution = resolver.resolve(plugin, "_workflow")

        assert resolution.found is True
        assert resolution.workflow is not None
        assert resolution.error is None

    def test_resolve_nonexistent_workflow(self, resolver, plugin):
        """Test resolving non-existent workflow."""
        resolution = resolver.resolve(plugin, "nonexistent_workflow")

        assert resolution.found is False
        assert resolution.workflow is None
        assert resolution.error is not None
        assert "not found" in resolution.error.lower()

    def test_resolve_invalid_workflow(self, resolver):
        """Test resolving workflow without execute method."""
        plugin = type("Plugin", (), {
            "metadata": type("Metadata", (), {"name": "test"})(),
            "invalid": InvalidWorkflow()
        })()

        resolution = resolver.resolve(plugin, "invalid")

        assert resolution.found is True
        assert resolution.workflow is not None
        assert resolution.error is not None
        assert "execute" in resolution.error.lower()

    def test_list_workflows(self, resolver, plugin):
        """Test listing all workflows in a plugin."""
        workflows = resolver.list_workflows(plugin)

        assert "booking_workflow" in workflows
        assert "search_workflow" in workflows

    def test_get_workflow_info(self, resolver):
        """Test getting workflow information."""
        workflow = DummyWorkflow()
        info = resolver.get_workflow_info(workflow)

        assert "name" in info
        assert "has_execute" in info
        assert info["has_execute"] is True
        assert "is_async" in info
        assert info["is_async"] is True
