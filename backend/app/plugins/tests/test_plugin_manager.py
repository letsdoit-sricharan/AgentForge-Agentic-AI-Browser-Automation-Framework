"""
Tests for PluginManager.
"""

import pytest

from app.plugins import (
    PluginManager,
    PluginNotFoundError,
    PluginStateError,
    PluginStatus,
)
from app.plugins.interfaces import PluginContext


class TestPluginManager:
    """Tests for PluginManager."""

    @pytest.fixture
    def manager(self):
        """Create a plugin manager instance."""
        return PluginManager()

    @pytest.fixture
    def plugin_context(self):
        """Create a mock plugin context."""
        return PluginContext(
            runtime=None,
            actions=None,
            memory=None,
            configuration=None,
            logger=None,
        )

    def test_load_plugin(self, manager):
        """Test loading a plugin."""
        manager.load_plugin("bookmyshow")

        assert manager.registry.has_plugin("bookmyshow")
        state = manager.get_plugin_state("bookmyshow")
        assert state.status == PluginStatus.LOADED

    def test_load_all_plugins(self, manager):
        """Test loading all plugins."""
        results = manager.load_all_plugins()

        assert isinstance(results, dict)
        assert "bookmyshow" in results
        assert results["bookmyshow"] is True

    def test_initialize_plugin(self, manager, plugin_context):
        """Test initializing a plugin."""
        manager.load_plugin("bookmyshow")
        manager.initialize_plugin("bookmyshow", plugin_context)

        state = manager.get_plugin_state("bookmyshow")
        assert state.status == PluginStatus.READY
        assert state.initialized_at is not None

    def test_initialize_unloaded_plugin_raises_error(self, manager, plugin_context):
        """Test that initializing an unloaded plugin raises an error."""
        manager.load_plugin("bookmyshow")
        # Don't initialize, try to execute directly

        with pytest.raises(PluginStateError):
            # Can't initialize from UNLOADED without loading first
            state = manager.get_plugin_state("bookmyshow")
            state.status = PluginStatus.UNLOADED  # Reset to unloaded
            manager.initialize_plugin("bookmyshow", plugin_context)

    def test_get_plugin(self, manager):
        """Test getting a plugin instance."""
        manager.load_plugin("bookmyshow")

        plugin = manager.get_plugin("bookmyshow")

        assert plugin is not None
        assert plugin.metadata.name == "bookmyshow"

    def test_get_nonexistent_plugin_raises_error(self, manager):
        """Test that getting a nonexistent plugin raises an error."""
        with pytest.raises(PluginNotFoundError):
            manager.get_plugin("nonexistent")

    def test_list_plugins(self, manager):
        """Test listing all plugins."""
        manager.load_plugin("bookmyshow")

        plugins = manager.list_plugins()

        assert isinstance(plugins, list)
        assert "bookmyshow" in plugins

    def test_find_plugins_by_capability(self, manager):
        """Test finding plugins by capability."""
        manager.load_plugin("bookmyshow")

        plugins = manager.find_plugins_by_capability("movie_booking")

        assert len(plugins) > 0
        assert any(p.metadata.name == "bookmyshow" for p in plugins)

    def test_shutdown_plugin(self, manager, plugin_context):
        """Test shutting down a plugin."""
        manager.load_plugin("bookmyshow")
        manager.initialize_plugin("bookmyshow", plugin_context)

        manager.shutdown_plugin("bookmyshow")

        state = manager.get_plugin_state("bookmyshow")
        assert state.status == PluginStatus.SHUTDOWN

    def test_shutdown_all_plugins(self, manager, plugin_context):
        """Test shutting down all plugins."""
        manager.load_plugin("bookmyshow")
        manager.initialize_plugin("bookmyshow", plugin_context)

        manager.shutdown_all_plugins()

        states = manager.get_all_plugin_states()
        for state in states.values():
            assert state.status == PluginStatus.SHUTDOWN
