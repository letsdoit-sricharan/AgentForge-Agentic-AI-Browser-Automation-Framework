"""
Tests for PluginContext.
"""

import pytest

from app.plugins.interfaces import PluginContext


class TestPluginContext:
    """Tests for PluginContext."""

    def test_create_context(self):
        """Test creating a plugin context."""
        context = PluginContext(
            runtime="runtime_mock",
            actions="actions_mock",
            memory="memory_mock",
            configuration="config_mock",
            logger="logger_mock",
        )

        assert context.runtime == "runtime_mock"
        assert context.actions == "actions_mock"
        assert context.memory == "memory_mock"
        assert context.configuration == "config_mock"
        assert context.logger == "logger_mock"

    def test_context_with_none_values(self):
        """Test that context can have None values."""
        context = PluginContext(
            runtime=None,
            actions=None,
            memory=None,
            configuration=None,
            logger=None,
        )

        assert context.runtime is None
        assert context.actions is None
        assert context.memory is None
        assert context.configuration is None
        assert context.logger is None

    def test_context_is_dataclass(self):
        """Test that PluginContext is a proper dataclass."""
        context = PluginContext(
            runtime="runtime",
            actions="actions",
            memory="memory",
            configuration="config",
            logger="logger",
        )

        # Dataclasses should have __dict__
        assert hasattr(context, "__dict__")

        # Test field access
        assert context.runtime == "runtime"
