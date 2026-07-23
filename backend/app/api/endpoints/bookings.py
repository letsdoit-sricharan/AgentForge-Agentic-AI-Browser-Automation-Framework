from typing import Dict, Any, Optional
import asyncio
from datetime import date
from uuid import uuid4

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel

from app.runtime.orchestrator.execution_orchestrator import ExecutionOrchestrator
from app.runtime.orchestrator.models import OrchestratedRequest
from app.plugins.manager.plugin_manager import PluginManager
from app.plugins.registry.plugin_registry import PluginRegistry
from app.plugins.bookmyshow.models.booking_request import BookingRequest
from app.browser_engine.implementations.playwright.playwright_adapter import PlaywrightAdapter
from app.browser_engine.implementations.playwright.playwright_browser import PlaywrightBrowser
from app.browser_engine.models.browser_options import BrowserOptions
from app.plugins.interfaces.plugin_context import PluginContext

router = APIRouter()

# Global state for tracking execution status
# In a real production system, this would be Redis or a Database.
_EXECUTION_STATE: Dict[str, Dict[str, Any]] = {}

# We create a global orchestrator and browser engine instance
plugin_registry = PluginRegistry()
plugin_manager = PluginManager(registry=plugin_registry)
plugin_manager.load_all_plugins()
orchestrator = ExecutionOrchestrator(plugin_manager)


class BookingInput(BaseModel):
    city: str
    movie: str
    show_date: date
    preferred_time: Optional[str] = None
    preferred_theatre: Optional[str] = None
    seat_preference: Optional[str] = None
    ticket_count: int = 1


async def execute_booking_task(request_id: str, booking_input: BookingInput):
    """
    Background task to execute the BookMyShow workflow.
    """
    _EXECUTION_STATE[request_id] = {
        "status": "RUNNING",
        "result": None,
        "errors": []
    }

    adapter = PlaywrightAdapter()
    browser = PlaywrightBrowser(adapter)
    
    try:
        options = BrowserOptions(
            headless=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        await browser.launch(options)
        
        session = await browser.new_session()
        page = await session.new_page()

        # Convert API input to the internal plugin model
        bms_request = BookingRequest(
            city=booking_input.city,
            movie=booking_input.movie,
            show_date=booking_input.show_date,
            preferred_time=booking_input.preferred_time,
            preferred_theatre=booking_input.preferred_theatre,
            seat_preference=booking_input.seat_preference,
            ticket_count=booking_input.ticket_count
        )

        orch_req = OrchestratedRequest(
            plugin_name="bookmyshow",
            workflow_name="booking_workflow",
            input_data={"booking_request": bms_request}
        )

        plugin_context = PluginContext(
            runtime=None, 
            actions=None, 
            memory=None, 
            configuration=None, 
            logger=None
        )
        
        # Execute the orchestrator
        result = await orchestrator.execute(
            request=orch_req,
            session=session,
            page=page,
            plugin_context=plugin_context
        )

        _EXECUTION_STATE[request_id]["status"] = "COMPLETED" if result.success else "FAILED"
        _EXECUTION_STATE[request_id]["result"] = result.output
        if not result.success:
            _EXECUTION_STATE[request_id]["errors"] = result.errors

    except Exception as e:
        _EXECUTION_STATE[request_id]["status"] = "FAILED"
        _EXECUTION_STATE[request_id]["errors"] = [str(e)]
    finally:
        await browser.close()


@router.post("/")
async def submit_booking(
    booking: BookingInput,
    background_tasks: BackgroundTasks
):
    request_id = str(uuid4())
    background_tasks.add_task(execute_booking_task, request_id, booking)
    return {"request_id": request_id, "status": "QUEUED"}


@router.get("/{request_id}")
async def get_booking_status(request_id: str):
    if request_id not in _EXECUTION_STATE:
        raise HTTPException(status_code=404, detail="Request ID not found")
    return _EXECUTION_STATE[request_id]
