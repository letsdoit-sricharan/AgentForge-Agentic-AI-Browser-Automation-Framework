"""
Tests for PluginLoader.
"""

import pytest

from app.plugins.exceptions import PluginLoadError, PluginValidationError
from app.plugins.manager import PluginLoader


class TestPluginLoader:
    """Tests for PluginLoader."""

    def test_discover_plugins(self):
        """Test discovering plugins in the plugins directory."""
        loader = PluginLoader(plugin_dir="app/plugins")

        plugins = loader.discover_plugins()

        # Should find at least the bookmyshow plugin
        assert isinstance(plugins, list)
        assert "bookmyshow" in plugins

    def test_load_plugin_success(self):
        """Test loading a valid plugin."""
        loader = PluginLoader(plugin_dir="app/plugins")

        plugin = loader.load_plugin("bookmyshow")

        assert plugin is not None
        assert hasattr(plugin, "metadata")
        assert plugin.metadata.name == "bookmyshow"
        assert hasattr(plugin, "initialize")
        assert hasattr(plugin, "execute")
        assert hasattr(plugin, "shutdown")

    def test_load_nonexistent_plugin_raises_error(self):
        """Test that loading a nonexistent plugin raises an error."""
        loader = PluginLoader(plugin_dir="app/plugins")

        with pytest.raises(PluginLoadError):
            loader.load_plugin("nonexistent_plugin")

    def test_load_all_plugins(self):
        """Test loading all available plugins."""
        loader = PluginLoader(plugin_dir="app/plugins")

        plugins = loader.load_all_plugins()

        assert isinstance(plugins, dict)
        assert "bookmyshow" in plugins

    def test_reload_plugin(self):
        """Test reloading a plugin."""
        loader = PluginLoader(plugin_dir="app/plugins")

        # Load once
        plugin1 = loader.load_plugin("bookmyshow")

        # Reload
        plugin2 = loader.reload_plugin("bookmyshow")

        assert plugin1 is not None
        assert plugin2 is not None
        assert plugin1.metadata.name == plugin2.metadata.name
