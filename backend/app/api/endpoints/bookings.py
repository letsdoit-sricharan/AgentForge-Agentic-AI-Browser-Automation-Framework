"""
Booking endpoints for the AgentForge/BookMyShow integration.

Endpoints
---------
POST /api/bookings/
    Submit a new booking request. Returns immediately with a ``request_id``
    that can be used to poll for status.

GET  /api/bookings/{request_id}
    Query the status of a previously submitted booking job.
"""

from __future__ import annotations

import logging
from datetime import date
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from pydantic import BaseModel, Field

from app.api.models.responses import (
    BookingStatus,
    BookingStatusResponse,
    BookingSubmittedResponse,
    WorkflowResultPayload,
)
from app.browser_engine.implementations.playwright.playwright_adapter import (
    PlaywrightAdapter,
)
from app.browser_engine.implementations.playwright.playwright_browser import (
    PlaywrightBrowser,
)
from app.browser_engine.models.browser_options import BrowserOptions
from app.plugins.bookmyshow.models.booking_request import BookingRequest
from app.plugins.interfaces.plugin_context import PluginContext
from app.plugins.manager.plugin_manager import PluginManager
from app.plugins.registry.plugin_registry import PluginRegistry
from app.runtime.orchestrator.execution_orchestrator import ExecutionOrchestrator
from app.runtime.orchestrator.models import OrchestratedRequest

logger = logging.getLogger(__name__)

router = APIRouter()

# ---------------------------------------------------------------------------
# In-process job store
# In a production system this would be backed by Redis or a database.
# ---------------------------------------------------------------------------
_EXECUTION_STATE: dict[str, dict[str, Any]] = {}

# ---------------------------------------------------------------------------
# Shared singleton infrastructure (created once at import time)
# ---------------------------------------------------------------------------
_plugin_registry = PluginRegistry()
_plugin_manager = PluginManager(registry=_plugin_registry)
_plugin_manager.load_all_plugins()
_orchestrator = ExecutionOrchestrator(_plugin_manager)


# ---------------------------------------------------------------------------
# Request model
# ---------------------------------------------------------------------------
class BookingInput(BaseModel):
    """
    Input payload for submitting a BookMyShow booking request.

    Example::

        {
            "city": "Mumbai",
            "movie": "Deadpool & Wolverine",
            "show_date": "2026-07-23",
            "ticket_count": 2,
            "preferred_time": "07:30 PM",
            "preferred_theatre": "PVR: Phoenix Palladium",
            "seat_preference": "any"
        }
    """

    city: str = Field(..., description="City in which to search for the movie.")
    movie: str = Field(..., description="Movie title to book.")
    show_date: date = Field(..., description="Date of the desired show (YYYY-MM-DD).")
    preferred_time: str | None = Field(
        None, description="Preferred show time, e.g. '07:30 PM'."
    )
    preferred_theatre: str | None = Field(
        None, description="Preferred theatre name."
    )
    seat_preference: str | None = Field(
        None, description="Seating preference, e.g. 'front', 'back', 'any'."
    )
    ticket_count: int = Field(1, ge=1, le=10, description="Number of tickets to book.")


# ---------------------------------------------------------------------------
# Background task
# ---------------------------------------------------------------------------
async def _execute_booking(request_id: str, booking_input: BookingInput) -> None:
    """
    Execute the full BookMyShow booking workflow in the background.

    Updates ``_EXECUTION_STATE[request_id]`` throughout the lifecycle so that
    ``GET /api/bookings/{request_id}`` can reflect progress.
    """
    _EXECUTION_STATE[request_id] = {
        "status": BookingStatus.RUNNING,
        "result": None,
        "errors": [],
    }
    logger.info("Starting booking job", extra={"request_id": request_id})

    adapter = PlaywrightAdapter()
    browser = PlaywrightBrowser(adapter)

    try:
        options = BrowserOptions(
            headless=True,
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        await browser.launch(options)

        session = await browser.new_session()
        page = await session.new_page()

        bms_request = BookingRequest(
            city=booking_input.city,
            movie=booking_input.movie,
            show_date=booking_input.show_date,
            preferred_time=booking_input.preferred_time,
            preferred_theatre=booking_input.preferred_theatre,
            seat_preference=booking_input.seat_preference,
            ticket_count=booking_input.ticket_count,
        )

        orch_req = OrchestratedRequest(
            plugin_name="bookmyshow",
            workflow_name="booking_workflow",
            input_data={"booking_request": bms_request},
        )

        plugin_context = PluginContext(
            runtime=None,
            actions=None,
            memory=None,
            configuration=None,
            logger=None,
        )

        result = await _orchestrator.execute(
            request=orch_req,
            session=session,
            page=page,
            plugin_context=plugin_context,
        )

        final_status = (
            BookingStatus.COMPLETED if result.success else BookingStatus.FAILED
        )
        _EXECUTION_STATE[request_id]["status"] = final_status
        _EXECUTION_STATE[request_id]["result"] = result.output

        if not result.success:
            _EXECUTION_STATE[request_id]["errors"] = result.errors

        logger.info(
            "Booking job finished",
            extra={"request_id": request_id, "status": final_status},
        )

    except Exception as exc:
        logger.exception(
            "Booking job raised an unhandled exception",
            extra={"request_id": request_id},
        )
        _EXECUTION_STATE[request_id]["status"] = BookingStatus.FAILED
        _EXECUTION_STATE[request_id]["errors"] = [str(exc)]

    finally:
        await browser.close()


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@router.post(
    "/",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=BookingSubmittedResponse,
    summary="Submit a booking request",
    description=(
        "Accepts a booking request and enqueues it for asynchronous execution. "
        "Returns a ``request_id`` that can be used to poll for status."
    ),
)
async def submit_booking(
    booking: BookingInput,
    background_tasks: BackgroundTasks,
) -> BookingSubmittedResponse:
    """
    Submit a new BookMyShow booking request.

    The request is executed asynchronously in the background. Poll
    ``GET /api/bookings/{request_id}`` to track progress.
    """
    request_id = str(uuid4())
    background_tasks.add_task(_execute_booking, request_id, booking)
    logger.info("Booking request queued", extra={"request_id": request_id})
    return BookingSubmittedResponse(request_id=request_id, status=BookingStatus.QUEUED)


@router.get(
    "/{request_id}",
    status_code=status.HTTP_200_OK,
    response_model=BookingStatusResponse,
    summary="Get booking status",
    description="Returns the current status and result of a previously submitted booking request.",
    responses={
        404: {"description": "No booking job found with the given request_id."},
    },
)
async def get_booking_status(request_id: str) -> BookingStatusResponse:
    """
    Retrieve the current status of a booking job.

    Returns ``QUEUED``, ``RUNNING``, ``COMPLETED``, or ``FAILED``
    along with the workflow result once the job finishes.
    """
    if request_id not in _EXECUTION_STATE:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking job '{request_id}' not found.",
        )

    state = _EXECUTION_STATE[request_id]
    raw_result = state.get("result")

    result_payload: WorkflowResultPayload | None = None
    if raw_result is not None:
        result_payload = WorkflowResultPayload(
            success=raw_result.get("success", False),
            message=raw_result.get("message", ""),
            data=raw_result.get("data", {}),
            error=raw_result.get("error"),
        )

    return BookingStatusResponse(
        status=state["status"],
        result=result_payload,
        errors=state.get("errors", []),
    )
