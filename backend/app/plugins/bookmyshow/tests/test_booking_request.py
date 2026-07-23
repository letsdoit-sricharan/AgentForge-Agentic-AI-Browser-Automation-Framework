"""
Tests for BookingRequest.

Run:
    python -m app.plugins.bookmyshow.tests.test_booking_request
"""

from datetime import date

from app.plugins.bookmyshow.models.booking_request import BookingRequest


def test_booking_request_creation() -> None:

    request = BookingRequest(
        city="Chennai",
        movie="Coolie",
        show_date=date(2026, 8, 15),
        preferred_time="7:00 PM",
        preferred_theatre="PVR Phoenix",
        seat_preference="Center",
        ticket_count=2,
    )

    assert request.city == "Chennai"
    assert request.movie == "Coolie"
    assert request.show_date == date(2026, 8, 15)
    assert request.preferred_time == "7:00 PM"
    assert request.preferred_theatre == "PVR Phoenix"
    assert request.seat_preference == "Center"
    assert request.ticket_count == 2

    print("✓ BookingRequest creation test passed.")


def test_default_values() -> None:

    request = BookingRequest(
        city="Hyderabad",
        movie="Coolie",
        show_date=date(2026, 8, 20),
    )

    assert request.preferred_time is None
    assert request.preferred_theatre is None
    assert request.seat_preference is None
    assert request.ticket_count == 1

    print("✓ BookingRequest default values test passed.")


def run_tests() -> None:

    print("\n" + "=" * 65)
    print("BookingRequest Tests")
    print("=" * 65)

    test_booking_request_creation()
    test_default_values()

    print("-" * 65)
    print("✅ All BookingRequest tests passed!")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()
