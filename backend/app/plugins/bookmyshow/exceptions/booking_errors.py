"""
Purpose:
    Defines BookMyShow-specific exceptions.

Responsibilities:
    - Represent business-level booking failures.
    - Provide a clear exception hierarchy for the plugin.

Does NOT:
    - Represent browser or framework failures.
"""

from __future__ import annotations


class BookMyShowError(Exception):
    """
    Base exception for all BookMyShow plugin errors.
    """


class InvalidBookingRequestError(BookMyShowError):
    """
    Raised when a booking request is invalid.
    """


class MovieNotFoundError(BookMyShowError):
    """
    Raised when the requested movie cannot be found.
    """


class TheatreNotFoundError(BookMyShowError):
    """
    Raised when the requested theatre cannot be found.
    """


class ShowUnavailableError(BookMyShowError):
    """
    Raised when the requested show is unavailable.
    """


class SeatUnavailableError(BookMyShowError):
    """
    Raised when the requested seats are unavailable.
    """


class PaymentFailedError(BookMyShowError):
    """
    Raised when payment cannot be completed.
    """


class TicketDownloadError(BookMyShowError):
    """
    Raised when the ticket cannot be downloaded.
    """