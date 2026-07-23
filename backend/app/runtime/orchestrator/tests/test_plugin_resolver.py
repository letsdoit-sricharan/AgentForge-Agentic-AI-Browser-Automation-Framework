"""
Tests for PluginResolver.
"""

import pytest

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins import PluginRegistry
from app.plugins.interfaces import Plugin, PluginContext, PluginMetadata
from app.runtime.orchestrator.exceptions import PluginResolutionError
from app.runtime.orchestrator.plugin_resolver import PluginResolver


class DummyPlugin(Plugin):
    """Mock plugin for testing."""

    def __init__(self, name: str = "test", capabilities: tuple = ()):
        self._metadata = PluginMetadata(
            name=name,
            version="1.0.0",
            description="Test plugin",
            author="Test",
            capabilities=capabilities,
        )

    @property
    def metadata(self):
        return self._metadata

    def initialize(self, context: PluginContext) -> None:
        pass

    async def execute(self, context: WorkflowContext):
        return {"status": "success"}

    def shutdown(self) -> None:
        pass


class TestPluginResolver:
    """Tests for PluginResolver."""

    @pytest.fixture
    def registry(self):
        """Create a plugin registry with test plugins."""
        registry = PluginRegistry()
        registry.register(DummyPlugin(name="plugin1", capabilities=("booking",)))
        registry.register(
            DummyPlugin(name="plugin2", capabilities=("booking", "search"))
        )
        registry.register(DummyPlugin(name="plugin3", capabilities=("search",)))
        return registry

    @pytest.fixture
    def resolver(self, registry):
        """Create a plugin resolver."""
        return PluginResolver(registry)

    def test_resolve_existing_plugin(self, resolver):
        """Test resolving an existing plugin."""
        resolution = resolver.resolve("plugin1")

        assert resolution.found is True
        assert resolution.plugin is not None
        assert resolution.plugin_name == "plugin1"
        assert resolution.error is None

    def test_resolve_nonexistent_plugin(self, resolver):
        """Test resolving a non-existent plugin."""
        resolution = resolver.resolve("nonexistent")

        assert resolution.found is False
        assert resolution.plugin is None
        assert resolution.error is not None
        assert "not found" in resolution.error.lower()

    def test_resolve_with_required_capabilities_success(self, resolver):
        """Test resolving with matching capabilities."""
        resolution = resolver.resolve("plugin2", required_capabilities=["booking", "search"])

        assert resolution.found is True
        assert resolution.plugin is not None
        assert resolution.error is None

    def test_resolve_with_required_capabilities_failure(self, resolver):
        """Test resolving with missing capabilities."""
        resolution = resolver.resolve("plugin1", required_capabilities=["booking", "payment"])

        assert resolution.found is True
        assert resolution.plugin is not None
        assert resolution.error is not None
        assert "missing required capabilities" in resolution.error.lower()

    def test_resolve_by_capability(self, resolver):
        """Test finding plugins by capability."""
        resolutions = resolver.resolve_by_capability("booking")

        assert len(resolutions) == 2
        plugin_names = [r.plugin_name for r in resolutions]
        assert "plugin1" in plugin_names
        assert "plugin2" in plugin_names

    def test_resolve_by_capability_no_results(self, resolver):
        """Test finding plugins by non-existent capability."""
        resolutions = resolver.resolve_by_capability("payment")

        assert len(resolutions) == 0

    def test_get_available_plugins(self, resolver):
        """Test getting all available plugins."""
        plugins = resolver.get_available_plugins()

        assert len(plugins) == 3
        assert "plugin1" in plugins
        assert "plugin2" in plugins
        assert "plugin3" in plugins

    def test_get_plugin_capabilities(self, resolver):
        """Test getting plugin capabilities."""
        capabilities = resolver.get_plugin_capabilities("plugin2")

        assert "booking" in capabilities
        assert "search" in capabilities

    def test_get_plugin_capabilities_not_found(self, resolver):
        """Test getting capabilities of non-existent plugin."""
        with pytest.raises(PluginResolutionError):
            resolver.get_plugin_capabilities("nonexistent")
