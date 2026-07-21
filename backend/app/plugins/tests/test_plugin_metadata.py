"""
Tests for PluginMetadata.
"""

import pytest

from app.plugins.interfaces import PluginMetadata


class TestPluginMetadata:
    """Tests for PluginMetadata."""

    def test_create_metadata(self):
        """Test creating plugin metadata."""
        metadata = PluginMetadata(
            name="test_plugin",
            version="1.0.0",
            description="A test plugin",
            author="Test Author",
        )

        assert metadata.name == "test_plugin"
        assert metadata.version == "1.0.0"
        assert metadata.description == "A test plugin"
        assert metadata.author == "Test Author"
        assert metadata.capabilities == ()
        assert metadata.homepage is None

    def test_create_metadata_with_capabilities(self):
        """Test creating metadata with capabilities."""
        metadata = PluginMetadata(
            name="test_plugin",
            version="1.0.0",
            description="A test plugin",
            author="Test Author",
            capabilities=("booking", "search", "payment"),
        )

        assert len(metadata.capabilities) == 3
        assert "booking" in metadata.capabilities
        assert "search" in metadata.capabilities
        assert "payment" in metadata.capabilities

    def test_create_metadata_with_homepage(self):
        """Test creating metadata with homepage."""
        metadata = PluginMetadata(
            name="test_plugin",
            version="1.0.0",
            description="A test plugin",
            author="Test Author",
            homepage="https://example.com",
        )

        assert metadata.homepage == "https://example.com"

    def test_metadata_is_immutable(self):
        """Test that metadata is immutable (frozen dataclass)."""
        metadata = PluginMetadata(
            name="test_plugin",
            version="1.0.0",
            description="A test plugin",
            author="Test Author",
        )

        with pytest.raises(AttributeError):
            metadata.name = "new_name"

    def test_metadata_equality(self):
        """Test metadata equality comparison."""
        metadata1 = PluginMetadata(
            name="test_plugin",
            version="1.0.0",
            description="A test plugin",
            author="Test Author",
        )

        metadata2 = PluginMetadata(
            name="test_plugin",
            version="1.0.0",
            description="A test plugin",
            author="Test Author",
        )

        assert metadata1 == metadata2

    def test_metadata_inequality(self):
        """Test metadata inequality comparison."""
        metadata1 = PluginMetadata(
            name="test_plugin",
            version="1.0.0",
            description="A test plugin",
            author="Test Author",
        )

        metadata2 = PluginMetadata(
            name="different_plugin",
            version="1.0.0",
            description="A test plugin",
            author="Test Author",
        )

        assert metadata1 != metadata2
