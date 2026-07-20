"""
Purpose:
    Defines the booking request model for the BookMyShow plugin.

Responsibilities:
    - Represent a user's ticket booking request.
    - Provide immutable booking information.
    - Act as the input to the booking workflow.

Does NOT:
    - Validate booking data.
    - Execute browser actions.
    - Contain website-specific logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True, slots=True)
class BookingRequest:
    """
    Represents a movie ticket booking request.
    """

    city: str

    movie: str

    show_date: date

    preferred_time: Optional[str] = None

    preferred_theatre: Optional[str] = None

    seat_preference: Optional[str] = None

    ticket_count: int = 1