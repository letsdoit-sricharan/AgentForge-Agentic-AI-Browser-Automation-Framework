"""
Tests for PluginRegistry.
"""

import pytest

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.exceptions import (
    PluginAlreadyRegisteredError,
    PluginNotFoundError,
)
from app.plugins.interfaces import Plugin, PluginContext, PluginMetadata
from app.plugins.models import PluginStatus
from app.plugins.registry import PluginRegistry


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


class TestPluginRegistry:
    """Tests for PluginRegistry."""

    def test_register_plugin(self):
        """Test registering a plugin."""
        registry = PluginRegistry()
        plugin = DummyPlugin(name="test_plugin")

        registry.register(plugin)

        assert registry.has_plugin("test_plugin")
        assert registry.count() == 1

    def test_register_duplicate_plugin_raises_error(self):
        """Test that registering a duplicate plugin raises an error."""
        registry = PluginRegistry()
        plugin = DummyPlugin(name="test_plugin")

        registry.register(plugin)

        with pytest.raises(PluginAlreadyRegisteredError):
            registry.register(plugin)

    def test_get_plugin(self):
        """Test getting a plugin by name."""
        registry = PluginRegistry()
        plugin = DummyPlugin(name="test_plugin")
        registry.register(plugin)

        retrieved = registry.get("test_plugin")

        assert retrieved == plugin
        assert retrieved.metadata.name == "test_plugin"

    def test_get_nonexistent_plugin_raises_error(self):
        """Test that getting a nonexistent plugin raises an error."""
        registry = PluginRegistry()

        with pytest.raises(PluginNotFoundError):
            registry.get("nonexistent")

    def test_unregister_plugin(self):
        """Test unregistering a plugin."""
        registry = PluginRegistry()
        plugin = DummyPlugin(name="test_plugin")
        registry.register(plugin)

        registry.unregister("test_plugin")

        assert not registry.has_plugin("test_plugin")
        assert registry.count() == 0

    def test_unregister_nonexistent_plugin_raises_error(self):
        """Test that unregistering a nonexistent plugin raises an error."""
        registry = PluginRegistry()

        with pytest.raises(PluginNotFoundError):
            registry.unregister("nonexistent")

    def test_get_state(self):
        """Test getting plugin state."""
        registry = PluginRegistry()
        plugin = DummyPlugin(name="test_plugin")
        registry.register(plugin)

        state = registry.get_state("test_plugin")

        assert state.plugin_name == "test_plugin"
        assert state.status == PluginStatus.UNLOADED

    def test_list_plugins(self):
        """Test listing all plugin names."""
        registry = PluginRegistry()
        registry.register(DummyPlugin(name="plugin1"))
        registry.register(DummyPlugin(name="plugin2"))

        plugin_names = [p.metadata.name for p in registry.get_all()]

        assert len(plugin_names) == 2
        assert "plugin1" in plugin_names
        assert "plugin2" in plugin_names

    def test_find_by_capability(self):
        """Test finding plugins by capability."""
        registry = PluginRegistry()
        registry.register(
            DummyPlugin(name="plugin1", capabilities=("booking", "search"))
        )
        registry.register(DummyPlugin(name="plugin2", capabilities=("booking",)))
        registry.register(DummyPlugin(name="plugin3", capabilities=("search",)))

        booking_plugins = registry.find_by_capability("booking")
        search_plugins = registry.find_by_capability("search")

        assert len(booking_plugins) == 2
        assert len(search_plugins) == 2

    def test_clear_registry(self):
        """Test clearing the registry."""
        registry = PluginRegistry()
        registry.register(DummyPlugin(name="plugin1"))
        registry.register(DummyPlugin(name="plugin2"))

        registry.clear()

        assert registry.count() == 0

    def test_get_plugins_by_status(self):
        """Test getting plugins by status."""
        registry = PluginRegistry()
        plugin = DummyPlugin(name="test_plugin")
        registry.register(plugin)

        unloaded_plugins = registry.get_plugins_by_status(PluginStatus.UNLOADED)

        assert len(unloaded_plugins) == 1
        assert unloaded_plugins[0].metadata.name == "test_plugin"
