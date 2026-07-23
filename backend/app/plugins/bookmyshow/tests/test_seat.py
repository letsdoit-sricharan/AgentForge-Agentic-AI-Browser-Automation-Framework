"""
Tests for Seat.

Run:
    python -m app.plugins.bookmyshow.tests.test_seat
"""

from app.plugins.bookmyshow.models.seat import Seat


def test_seat_creation() -> None:
    """
    Test creating a seat.
    """

    seat = Seat(
        seat_number="G10",
        row="G",
        category="Premium",
        price=250.0,
        is_available=True,
    )

    assert seat.seat_number == "G10"
    assert seat.row == "G"
    assert seat.category == "Premium"
    assert seat.price == 250.0
    assert seat.is_available is True

    print("✓ Seat creation test passed.")


def test_default_values() -> None:
    """
    Test default values.
    """

    seat = Seat(
        seat_number="A1",
    )

    assert seat.row is None
    assert seat.category is None
    assert seat.price is None
    assert seat.is_available is True

    print("✓ Seat default values test passed.")


def run_tests() -> None:

    print("\n" + "=" * 65)
    print("Seat Tests")
    print("=" * 65)

    test_seat_creation()
    test_default_values()

    print("-" * 65)
    print("✅ All Seat tests passed!")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()
