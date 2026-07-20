# Payment model
"""
Purpose:
    Defines the payment model for the BookMyShow plugin.

Responsibilities:
    - Represent payment information.
    - Track payment status.
    - Store payment-related metadata.

Does NOT:
    - Process payments.
    - Execute browser actions.
    - Communicate with payment gateways.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PaymentStatus(Enum):
    """
    Represents the current payment state.
    """

    PENDING = "pending"
    INITIATED = "initiated"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class Payment:
    """
    Represents payment information for a booking.
    """

    amount: float

    currency: str = "INR"

    status: PaymentStatus = PaymentStatus.PENDING

    transaction_id: str | None = None

    payment_url: str | None = None