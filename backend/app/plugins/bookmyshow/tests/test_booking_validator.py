"""
Tests for BookingValidator.

Run:
    python -m app.plugins.bookmyshow.tests.test_booking_validator
"""

from datetime import date

from app.plugins.bookmyshow.models.booking_request import BookingRequest
from app.plugins.bookmyshow.validators.booking_validator import (
    BookingValidator,
)


validator = BookingValidator()


def test_valid_request() -> None:

    request = BookingRequest(
        city="Chennai",
        movie="Coolie",
        show_date=date(2026, 8, 15),
        ticket_count=2,
    )

    result = validator.validate(request)

    assert result.valid is True

    print("✓ Valid request test passed.")


def test_empty_city() -> None:

    request = BookingRequest(
        city="",
        movie="Coolie",
        show_date=date(2026, 8, 15),
    )

    result = validator.validate(request)

    assert result.valid is False

    print("✓ Empty city test passed.")


def test_empty_movie() -> None:

    request = BookingRequest(
        city="Chennai",
        movie="",
        show_date=date(2026, 8, 15),
    )

    result = validator.validate(request)

    assert result.valid is False

    print("✓ Empty movie test passed.")


def test_invalid_ticket_count() -> None:

    request = BookingRequest(
        city="Chennai",
        movie="Coolie",
        show_date=date(2026, 8, 15),
        ticket_count=0,
    )

    result = validator.validate(request)

    assert result.valid is False

    print("✓ Invalid ticket count test passed.")


def test_ticket_limit() -> None:

    request = BookingRequest(
        city="Chennai",
        movie="Coolie",
        show_date=date(2026, 8, 15),
        ticket_count=11,
    )

    result = validator.validate(request)

    assert result.valid is False

    print("✓ Ticket limit test passed.")


def run_tests() -> None:

    print("\n" + "=" * 65)
    print("BookingValidator Tests")
    print("=" * 65)

    test_valid_request()
    test_empty_city()
    test_empty_movie()
    test_invalid_ticket_count()
    test_ticket_limit()

    print("-" * 65)
    print("✅ All BookingValidator tests passed!")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()