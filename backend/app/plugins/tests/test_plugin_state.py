"""
Tests for PluginState.
"""

from datetime import datetime

from app.plugins.models import PluginState, PluginStatus


class TestPluginState:
    """Tests for PluginState."""

    def test_initial_state(self):
        """Test that initial state is UNLOADED."""
        state = PluginState(plugin_name="test_plugin")

        assert state.plugin_name == "test_plugin"
        assert state.status == PluginStatus.UNLOADED
        assert state.loaded_at is None
        assert state.initialized_at is None
        assert state.last_executed_at is None
        assert state.execution_count == 0

    def test_mark_loading(self):
        """Test marking plugin as loading."""
        state = PluginState(plugin_name="test_plugin")

        state.mark_loading()

        assert state.status == PluginStatus.LOADING
        assert state.error is None

    def test_mark_loaded(self):
        """Test marking plugin as loaded."""
        state = PluginState(plugin_name="test_plugin")

        state.mark_loaded()

        assert state.status == PluginStatus.LOADED
        assert state.loaded_at is not None
        assert isinstance(state.loaded_at, datetime)

    def test_mark_initializing(self):
        """Test marking plugin as initializing."""
        state = PluginState(plugin_name="test_plugin")

        state.mark_initializing()

        assert state.status == PluginStatus.INITIALIZING

    def test_mark_ready(self):
        """Test marking plugin as ready."""
        state = PluginState(plugin_name="test_plugin")

        state.mark_ready()

        assert state.status == PluginStatus.READY
        assert state.initialized_at is not None

    def test_mark_executing(self):
        """Test marking plugin as executing."""
        state = PluginState(plugin_name="test_plugin")

        state.mark_executing()

        assert state.status == PluginStatus.EXECUTING

    def test_mark_execution_complete(self):
        """Test marking plugin execution as complete."""
        state = PluginState(plugin_name="test_plugin")

        state.mark_execution_complete()

        assert state.status == PluginStatus.READY
        assert state.last_executed_at is not None
        assert state.execution_count == 1

    def test_multiple_executions(self):
        """Test tracking multiple executions."""
        state = PluginState(plugin_name="test_plugin")

        state.mark_execution_complete()
        state.mark_execution_complete()
        state.mark_execution_complete()

        assert state.execution_count == 3

    def test_mark_error(self):
        """Test marking plugin as errored."""
        state = PluginState(plugin_name="test_plugin")
        error = Exception("Test error")

        state.mark_error(error)

        assert state.status == PluginStatus.ERROR
        assert state.error == error

    def test_mark_shutting_down(self):
        """Test marking plugin as shutting down."""
        state = PluginState(plugin_name="test_plugin")

        state.mark_shutting_down()

        assert state.status == PluginStatus.SHUTTING_DOWN

    def test_mark_shutdown(self):
        """Test marking plugin as shut down."""
        state = PluginState(plugin_name="test_plugin")

        state.mark_shutdown()

        assert state.status == PluginStatus.SHUTDOWN

    def test_can_initialize_from_loaded(self):
        """Test that plugin can be initialized from LOADED state."""
        state = PluginState(plugin_name="test_plugin")
        state.mark_loaded()

        assert state.can_initialize() is True

    def test_cannot_initialize_from_unloaded(self):
        """Test that plugin cannot be initialized from UNLOADED state."""
        state = PluginState(plugin_name="test_plugin")

        assert state.can_initialize() is False

    def test_can_execute_from_ready(self):
        """Test that plugin can execute from READY state."""
        state = PluginState(plugin_name="test_plugin")
        state.mark_ready()

        assert state.can_execute() is True

    def test_cannot_execute_from_unloaded(self):
        """Test that plugin cannot execute from UNLOADED state."""
        state = PluginState(plugin_name="test_plugin")

        assert state.can_execute() is False

    def test_can_shutdown_from_ready(self):
        """Test that plugin can be shut down from READY state."""
        state = PluginState(plugin_name="test_plugin")
        state.mark_ready()

        assert state.can_shutdown() is True

    def test_can_shutdown_from_error(self):
        """Test that plugin can be shut down from ERROR state."""
        state = PluginState(plugin_name="test_plugin")
        state.mark_error(Exception("Test error"))

        assert state.can_shutdown() is True


class TestPluginStatus:
    """Tests for PluginStatus enum."""

    def test_status_values(self):
        """Test that all expected status values exist."""
        expected_statuses = [
            "UNLOADED",
            "LOADING",
            "LOADED",
            "INITIALIZING",
            "READY",
            "EXECUTING",
            "ERROR",
            "SHUTTING_DOWN",
            "SHUTDOWN",
        ]

        for status_name in expected_statuses:
            assert hasattr(PluginStatus, status_name)

    def test_status_enum_values(self):
        """Test that status enum values are unique."""
        statuses = list(PluginStatus)
        assert len(statuses) == len(set(statuses))
