"""
Purpose:
    Defines the theatre model for the BookMyShow plugin.

Responsibilities:
    - Represent a theatre.
    - Store theatre information.
    - Act as a reusable domain model.

Does NOT:
    - Execute browser actions.
    - Search for theatres.
    - Contain website-specific logic.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Theatre:
    """
    Represents a movie theatre.
    """

    name: str

    address: str | None = None

    distance_km: float | None = None

    is_available: bool = True