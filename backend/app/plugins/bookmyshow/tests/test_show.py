"""
Tests for Show.

Run:
    python -m app.plugins.bookmyshow.tests.test_show
"""

from datetime import date

from app.plugins.bookmyshow.models.show import Show
from app.plugins.bookmyshow.models.theatre import Theatre


def test_show_creation() -> None:
    """
    Test creating a movie show.
    """

    theatre = Theatre(
        name="PVR Phoenix",
        address="Velachery, Chennai",
    )

    show = Show(
        movie="Coolie",
        theatre=theatre,
        show_date=date(2026, 8, 15),
        show_time="7:00 PM",
        language="Tamil",
        screen_type="IMAX",
        is_available=True,
    )

    assert show.movie == "Coolie"
    assert show.theatre == theatre
    assert show.show_date == date(2026, 8, 15)
    assert show.show_time == "7:00 PM"
    assert show.language == "Tamil"
    assert show.screen_type == "IMAX"
    assert show.is_available is True

    print("✓ Show creation test passed.")


def test_show_default_values() -> None:
    """
    Test default values.
    """

    theatre = Theatre(name="INOX")

    show = Show(
        movie="Coolie",
        theatre=theatre,
        show_date=date(2026, 8, 15),
        show_time="10:30 PM",
    )

    assert show.language is None
    assert show.screen_type is None
    assert show.is_available is True

    print("✓ Show default values test passed.")


def run_tests() -> None:

    print("\n" + "=" * 65)
    print("Show Tests")
    print("=" * 65)

    test_show_creation()
    test_show_default_values()

    print("-" * 65)
    print("✅ All Show tests passed!")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()
