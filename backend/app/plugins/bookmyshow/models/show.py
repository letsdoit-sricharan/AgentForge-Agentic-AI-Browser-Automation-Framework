"""
Purpose:
    Defines the movie show model for the BookMyShow plugin.

Responsibilities:
    - Represent a movie show.
    - Store show information.
    - Reference the theatre where the show is available.

Does NOT:
    - Execute browser actions.
    - Search for movie shows.
    - Contain website-specific logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.plugins.bookmyshow.models.theatre import Theatre


@dataclass(frozen=True)
class Show:
    """
    Represents a movie show.
    """

    movie: str

    theatre: Theatre

    show_date: date

    show_time: str

    language: str | None = None

    screen_type: str | None = None

    is_available: bool = True
