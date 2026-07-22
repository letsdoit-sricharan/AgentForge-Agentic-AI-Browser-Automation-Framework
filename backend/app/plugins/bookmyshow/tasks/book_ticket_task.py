"""
Task implementation for booking a movie ticket on BookMyShow.
"""

from __future__ import annotations

from typing import Any
from datetime import date

from app.runtime.tasks.task import Task


from dataclasses import dataclass

@dataclass
class BookTicketTask(Task):
    """
    Task to book a movie ticket.
    """

    city: str
    movie: str
    show_date: date
    preferred_time: str | None = None
    preferred_theatre: str | None = None
    seat_preference: str | None = None
    ticket_count: int = 1

    @property
    def task_type(self) -> str:
        return "booking"

    def validate(self) -> tuple[bool, list[str]]:
        errors = []
        if not self.city:
            errors.append("City is required.")
        if not self.movie:
            errors.append("Movie name is required.")
        if not self.show_date:
            errors.append("Show date is required.")
        
        return len(errors) == 0, errors

    def to_dict(self) -> dict[str, Any]:
        from app.plugins.bookmyshow.models.booking_request import BookingRequest
        
        request = BookingRequest(
            city=self.city,
            movie=self.movie,
            show_date=self.show_date,
            preferred_time=self.preferred_time,
            preferred_theatre=self.preferred_theatre,
            seat_preference=self.seat_preference,
            ticket_count=self.ticket_count,
        )
        return {
            "booking_request": request
        }
