"""
Tests for TaskRegistry.
"""

import pytest

from app.runtime.tasks.exceptions import (
    TaskNotSupportedError,
)
from app.runtime.tasks.task_metadata import TaskMetadata
from app.runtime.tasks.task_registry import TaskRegistry


class TestTaskRegistry:
    """Tests for TaskRegistry."""

    @pytest.fixture
    def registry(self):
        """Create a task registry."""
        return TaskRegistry()

    @pytest.fixture
    def metadata(self):
        """Create sample task metadata."""
        return TaskMetadata(
            task_type="search_movie",
            name="Search Movie",
            description="Search for a movie",
            required_inputs=("movie", "city"),
        )

    def test_register_task(self, registry, metadata):
        """Test registering a task."""
        registry.register_task("search_movie", "bookmyshow", metadata)

        assert registry.is_task_supported("search_movie")
        plugins = registry.get_supporting_plugins("search_movie")
        assert "bookmyshow" in plugins

    def test_register_multiple_plugins_for_task(self, registry):
        """Test multiple plugins supporting the same task."""
        registry.register_task("search_movie", "bookmyshow")
        registry.register_task("search_movie", "paytm")

        plugins = registry.get_supporting_plugins("search_movie")
        assert len(plugins) == 2
        assert "bookmyshow" in plugins
        assert "paytm" in plugins

    def test_get_supporting_plugins_not_found(self, registry):
        """Test getting plugins for unsupported task."""
        with pytest.raises(TaskNotSupportedError):
            registry.get_supporting_plugins("nonexistent_task")

    def test_is_task_supported(self, registry):
        """Test checking if task is supported."""
        assert not registry.is_task_supported("search_movie")

        registry.register_task("search_movie", "bookmyshow")

        assert registry.is_task_supported("search_movie")

    def test_get_plugin_tasks(self, registry):
        """Test getting tasks supported by a plugin."""
        registry.register_task("search_movie", "bookmyshow")
        registry.register_task("select_seats", "bookmyshow")

        tasks = registry.get_plugin_tasks("bookmyshow")
        assert len(tasks) == 2
        assert "search_movie" in tasks
        assert "select_seats" in tasks

    def test_get_task_metadata(self, registry, metadata):
        """Test getting task metadata."""
        registry.register_task("search_movie", "bookmyshow", metadata)

        retrieved = registry.get_task_metadata("search_movie")
        assert retrieved == metadata

    def test_get_task_metadata_not_found(self, registry):
        """Test getting metadata for unregistered task."""
        result = registry.get_task_metadata("nonexistent")
        assert result is None

    def test_unregister_task(self, registry):
        """Test unregistering a task."""
        registry.register_task("search_movie", "bookmyshow")
        registry.unregister_task("search_movie", "bookmyshow")

        assert not registry.is_task_supported("search_movie")

    def test_unregister_one_plugin_keeps_others(self, registry):
        """Test unregistering one plugin keeps task for others."""
        registry.register_task("search_movie", "bookmyshow")
        registry.register_task("search_movie", "paytm")

        registry.unregister_task("search_movie", "bookmyshow")

        assert registry.is_task_supported("search_movie")
        plugins = registry.get_supporting_plugins("search_movie")
        assert "paytm" in plugins
        assert "bookmyshow" not in plugins

    def test_get_all_task_types(self, registry):
        """Test getting all task types."""
        registry.register_task("search_movie", "bookmyshow")
        registry.register_task("select_seats", "bookmyshow")

        tasks = registry.get_all_task_types()
        assert len(tasks) == 2
        assert "search_movie" in tasks
        assert "select_seats" in tasks

    def test_get_all_plugins(self, registry):
        """Test getting all plugins."""
        registry.register_task("search_movie", "bookmyshow")
        registry.register_task("search_product", "amazon")

        plugins = registry.get_all_plugins()
        assert len(plugins) == 2
        assert "bookmyshow" in plugins
        assert "amazon" in plugins

    def test_clear(self, registry):
        """Test clearing registry."""
        registry.register_task("search_movie", "bookmyshow")
        registry.clear()

        assert len(registry.get_all_task_types()) == 0
        assert len(registry.get_all_plugins()) == 0

    def test_get_statistics(self, registry):
        """Test getting registry statistics."""
        registry.register_task("search_movie", "bookmyshow")
        registry.register_task("select_seats", "bookmyshow")

        stats = registry.get_statistics()
        assert stats["total_tasks"] == 2
        assert stats["total_plugins"] == 1
