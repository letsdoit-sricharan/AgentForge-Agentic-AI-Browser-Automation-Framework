"""
Purpose:
    Defines the booking result model for the BookMyShow plugin.

Responsibilities:
    - Represent the outcome of a booking workflow.
    - Store booking information.
    - Store failure information when booking is unsuccessful.

Does NOT:
    - Execute browser actions.
    - Validate booking requests.
    - Contain website-specific logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class BookingResult:
    """
    Represents the outcome of a movie ticket booking.
    """

    success: bool

    message: str = ""

    booking_id: str | None = None

    ticket_url: str | None = None

    theatre: str | None = None

    show_time: str | None = None

    seats: tuple[str, ...] = ()

    data: dict[str, Any] = field(default_factory=dict)

    error: Exception | None = None
