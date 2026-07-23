"""
Purpose:
    Validates booking requests for the BookMyShow plugin.

Responsibilities:
    - Validate BookingRequest instances.
    - Return ValidationResult objects.

Does NOT:
    - Execute browser actions.
    - Perform bookings.
    - Access BookMyShow.
"""

from __future__ import annotations

from app.plugin_framework.validators import (
    ValidationResult,
    Validator,
)
from app.plugins.bookmyshow.models.booking_request import (
    BookingRequest,
)


class BookingValidator(Validator):
    """
    Validates BookingRequest objects.
    """

    @property
    def name(self) -> str:
        return "booking_validator"

    def validate(
        self,
        data: BookingRequest,
    ) -> ValidationResult:
        """
        Validate a booking request.
        """

        if not data.city.strip():
            return ValidationResult(
                valid=False,
                message="City is required.",
            )

        if not data.movie.strip():
            return ValidationResult(
                valid=False,
                message="Movie name is required.",
            )

        if data.ticket_count <= 0:
            return ValidationResult(
                valid=False,
                message="Ticket count must be greater than zero.",
            )

        if data.ticket_count > 10:
            return ValidationResult(
                valid=False,
                message="A maximum of 10 tickets can be booked.",
            )

        if data.show_date is None:
            return ValidationResult(
                valid=False,
                message="Show date is required.",
            )

        return ValidationResult(
            valid=True,
            message="Booking request is valid.",
        )
