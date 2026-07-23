"""
Tests for BookMyShow exceptions.
"""

from app.plugins.bookmyshow.exceptions.booking_errors import (
    BookMyShowError,
    InvalidBookingRequestError,
    MovieNotFoundError,
    PaymentFailedError,
    SeatUnavailableError,
    ShowUnavailableError,
    TheatreNotFoundError,
    TicketDownloadError,
)


def test_exception_hierarchy() -> None:

    assert issubclass(InvalidBookingRequestError, BookMyShowError)
    assert issubclass(MovieNotFoundError, BookMyShowError)
    assert issubclass(TheatreNotFoundError, BookMyShowError)
    assert issubclass(ShowUnavailableError, BookMyShowError)
    assert issubclass(SeatUnavailableError, BookMyShowError)
    assert issubclass(PaymentFailedError, BookMyShowError)
    assert issubclass(TicketDownloadError, BookMyShowError)

    print("✓ Exception hierarchy test passed.")


def run_tests() -> None:

    print("\n" + "=" * 70)
    print("BookMyShow Exception Tests")
    print("=" * 70)

    test_exception_hierarchy()

    print("-" * 70)
    print("✅ All exception tests passed!")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
