"""
Tests for BookMyShow plugin metadata.

Run:
    python -m app.plugins.bookmyshow.tests.test_metadata
"""

from app.plugins.bookmyshow.metadata import BOOKMYSHOW_METADATA


def test_metadata() -> None:

    assert BOOKMYSHOW_METADATA.name == "bookmyshow"

    assert BOOKMYSHOW_METADATA.version == "1.0.0"

    assert BOOKMYSHOW_METADATA.author == "AgentForge"

    assert "movie_booking" in BOOKMYSHOW_METADATA.capabilities

    assert "seat_selection" in BOOKMYSHOW_METADATA.capabilities

    print("✓ BookMyShow metadata test passed.")


def run_tests() -> None:

    print("\n" + "=" * 65)
    print("BookMyShow Metadata Tests")
    print("=" * 65)

    test_metadata()

    print("-" * 65)
    print("✅ All BookMyShow metadata tests passed!")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()
    