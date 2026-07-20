"""
Purpose:
    Defines the seat model for the BookMyShow plugin.

Responsibilities:
    - Represent a theatre seat.
    - Store seat information.
    - Indicate seat availability.

Does NOT:
    - Execute browser actions.
    - Select seats.
    - Contain website-specific logic.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Seat:
    """
    Represents a theatre seat.
    """

    seat_number: str

    row: str | None = None

    category: str | None = None

    price: float | None = None

    is_available: bool = True