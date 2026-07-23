"""
Shared Pydantic response models for the AgentForge API.

All endpoints return one of these standard envelopes to ensure
a consistent, versioned contract for API consumers.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class BookingStatus(str, Enum):
    """Lifecycle states of an asynchronous booking job."""

    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class BookingSubmittedResponse(BaseModel):
    """
    Returned immediately after a booking request is accepted.

    The ``request_id`` can be used to poll ``GET /api/bookings/{request_id}``
    for status updates.

    Example::

        {
            "request_id": "c8b49b4a-b7d9-425a-9e6d-ef74d9c911ab",
            "status": "QUEUED"
        }
    """

    request_id: str = Field(..., description="Unique identifier for this booking job.")
    status: BookingStatus = Field(
        BookingStatus.QUEUED,
        description="Initial job status — always QUEUED.",
    )


class WorkflowResultPayload(BaseModel):
    """
    Serialised outcome of a completed workflow execution.

    Present in ``BookingStatusResponse`` only when ``status`` is
    ``COMPLETED`` or ``FAILED``.
    """

    success: bool = Field(..., description="Whether the workflow finished successfully.")
    message: str = Field(..., description="Human-readable result summary.")
    data: dict[str, Any] = Field(
        default_factory=dict,
        description="Structured output produced by the workflow.",
    )
    error: Optional[str] = Field(None, description="Error detail if the workflow failed.")


class BookingStatusResponse(BaseModel):
    """
    Returned by ``GET /api/bookings/{request_id}``.

    Example (running)::

        {"status": "RUNNING", "result": null, "errors": []}

    Example (completed)::

        {
            "status": "COMPLETED",
            "result": {
                "success": true,
                "message": "Booking workflow completed successfully.",
                "data": {},
                "error": null
            },
            "errors": []
        }
    """

    status: BookingStatus = Field(..., description="Current lifecycle state of the job.")
    result: Optional[WorkflowResultPayload] = Field(
        None,
        description="Workflow outcome — populated once the job finishes.",
    )
    errors: list[str] = Field(
        default_factory=list,
        description="Non-fatal error messages accumulated during execution.",
    )
