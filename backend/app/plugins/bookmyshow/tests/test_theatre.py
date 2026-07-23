"""
Tests for Theatre.

Run:
    python -m app.plugins.bookmyshow.tests.test_theatre
"""

from app.plugins.bookmyshow.models.theatre import Theatre


def test_theatre_creation() -> None:
    """
    Test theatre creation.
    """

    theatre = Theatre(
        name="PVR Phoenix",
        address="Velachery, Chennai",
        distance_km=4.2,
        is_available=True,
    )

    assert theatre.name == "PVR Phoenix"
    assert theatre.address == "Velachery, Chennai"
    assert theatre.distance_km == 4.2
    assert theatre.is_available is True

    print("✓ Theatre creation test passed.")


def test_default_values() -> None:
    """
    Test default field values.
    """

    theatre = Theatre(name="INOX Marina")

    assert theatre.address is None
    assert theatre.distance_km is None
    assert theatre.is_available is True

    print("✓ Theatre default values test passed.")


def run_tests() -> None:

    print("\n" + "=" * 65)
    print("Theatre Tests")
    print("=" * 65)

    test_theatre_creation()
    test_default_values()

    print("-" * 65)
    print("✅ All Theatre tests passed!")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()
