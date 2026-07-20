"""
Tests for BookingResult.

Run:
    python -m app.plugins.bookmyshow.tests.test_booking_result
"""

from app.plugins.bookmyshow.models.booking_result import BookingResult


def test_successful_booking_result() -> None:
    """
    Test a successful booking result.
    """

    result = BookingResult(
        success=True,
        message="Booking completed successfully.",
        booking_id="BMS123456",
        ticket_url="https://bookmyshow.com/ticket/123456",
        theatre="PVR Phoenix",
        show_time="7:00 PM",
        seats=("G10", "G11"),
    )

    assert result.success is True
    assert result.booking_id == "BMS123456"
    assert result.theatre == "PVR Phoenix"
    assert result.show_time == "7:00 PM"
    assert result.seats == ("G10", "G11")
    assert result.error is None

    print("✓ Successful BookingResult test passed.")


def test_failed_booking_result() -> None:
    """
    Test a failed booking result.
    """

    error = RuntimeError("Show unavailable.")

    result = BookingResult(
        success=False,
        message="Booking failed.",
        error=error,
    )

    assert result.success is False
    assert result.message == "Booking failed."
    assert result.error is error
    assert result.booking_id is None
    assert result.seats == ()

    print("✓ Failed BookingResult test passed.")


def test_default_values() -> None:
    """
    Test default values.
    """

    result = BookingResult(success=True)

    assert result.message == ""
    assert result.booking_id is None
    assert result.ticket_url is None
    assert result.theatre is None
    assert result.show_time is None
    assert result.seats == ()
    assert result.data == {}
    assert result.error is None

    print("✓ BookingResult default values test passed.")


def run_tests() -> None:

    print("\n" + "=" * 65)
    print("BookingResult Tests")
    print("=" * 65)

    test_successful_booking_result()
    test_failed_booking_result()
    test_default_values()

    print("-" * 65)
    print("✅ All BookingResult tests passed!")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()