"""
Tests for PluginMetadata.

Run:
    python -m app.plugins.tests.test_plugin_metadata
"""

from dataclasses import FrozenInstanceError

from app.plugins.interfaces import PluginMetadata


def test_plugin_metadata_creation() -> None:
    """Verify that metadata is created correctly."""

    metadata = PluginMetadata(
        name="bookmyshow",
        version="1.0.0",
        description="Movie ticket booking automation",
        author="AgentForge",
        capabilities=(
            "movie_search",
            "seat_selection",
            "ticket_booking",
        ),
    )

    assert metadata.name == "bookmyshow"
    assert metadata.version == "1.0.0"
    assert metadata.description == "Movie ticket booking automation"
    assert metadata.author == "AgentForge"
    assert len(metadata.capabilities) == 3

    print("✓ Plugin metadata creation test passed.")


def test_plugin_metadata_defaults() -> None:
    """Verify default values."""

    metadata = PluginMetadata(
        name="dummy",
        version="0.1.0",
        description="Dummy plugin",
        author="AgentForge",
    )

    assert metadata.capabilities == ()
    assert metadata.homepage is None

    print("✓ Plugin metadata default values test passed.")


def test_plugin_metadata_immutable() -> None:
    """Verify metadata is immutable."""

    metadata = PluginMetadata(
        name="dummy",
        version="0.1.0",
        description="Dummy plugin",
        author="AgentForge",
    )

    try:
        metadata.name = "changed"
    except FrozenInstanceError:
        print("✓ Plugin metadata immutability test passed.")
    else:
        raise AssertionError("PluginMetadata should be immutable.")


def run_tests() -> None:
    """Execute all PluginMetadata tests."""

    print("\n" + "=" * 60)
    print("Running PluginMetadata Tests")
    print("=" * 60)

    test_plugin_metadata_creation()
    test_plugin_metadata_defaults()
    test_plugin_metadata_immutable()

    print("-" * 60)
    print("✅ All PluginMetadata tests passed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()