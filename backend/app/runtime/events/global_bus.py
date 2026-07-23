"""
Global Event Bus

Provides a singleton EventBus for the API and Workflows to communicate
without tight coupling. Also hosts an in-memory event store to persist
execution timelines.
"""

from __future__ import annotations

import logging
from typing import Any

from app.runtime.events.event_bus import EventBus
from app.runtime.events.workflow_event import WorkflowEvent
from app.runtime.events.event_handlers import EventHandler

logger = logging.getLogger(__name__)

# Singleton Event Bus instance
global_bus = EventBus()

# In-memory storage for events: { execution_id: list[WorkflowEvent] }
_EVENT_STORE: dict[str, list[WorkflowEvent]] = {}


class StoreEventHandler(EventHandler):
    """
    Automatically stores any published WorkflowEvent into the in-memory store.
    """
    def handle(self, event: Any) -> None:
        if isinstance(event, WorkflowEvent):
            exec_id = event.execution_id
            if exec_id not in _EVENT_STORE:
                _EVENT_STORE[exec_id] = []
            _EVENT_STORE[exec_id].append(event)
            logger.debug(f"Stored event {event.event_type.value} for {exec_id}")

# Subscribe the global store handler immediately
_store_handler = StoreEventHandler()
global_bus.subscribe(_store_handler)


def get_execution_events(execution_id: str) -> list[WorkflowEvent]:
    """Retrieve all events for a specific execution."""
    return _EVENT_STORE.get(execution_id, [])


def get_all_executions() -> list[dict[str, Any]]:
    """
    Aggregate the in-memory events to determine high-level execution states.
    Returns a list of summaries for all executions.
    """
    from app.runtime.events.event_types import WorkflowEventType
    
    executions = []
    for exec_id, events in _EVENT_STORE.items():
        if not events:
            continue
            
        started_event = next((e for e in events if e.event_type == WorkflowEventType.WORKFLOW_STARTED), None)
        completed_event = next((e for e in events if e.event_type in (WorkflowEventType.WORKFLOW_COMPLETED, WorkflowEventType.WORKFLOW_FAILED)), None)
        
        # Deduce status
        status = "QUEUED"
        if completed_event:
            status = "COMPLETED" if completed_event.event_type == WorkflowEventType.WORKFLOW_COMPLETED else "FAILED"
        elif started_event:
            status = "RUNNING"
            
        started_at = started_event.timestamp if started_event else events[0].timestamp
        completed_at = completed_event.timestamp if completed_event else None
        
        duration = 0
        if started_at and completed_at:
            duration = int((completed_at - started_at).total_seconds())
        elif started_at:
            from datetime import datetime, timezone
            duration = int((datetime.now(timezone.utc) - started_at).total_seconds())

        executions.append({
            "id": exec_id,
            "plugin": events[0].payload.get("plugin_name", "Unknown"),
            "status": status,
            "started_at": started_at.isoformat() if started_at else None,
            "completed_at": completed_at.isoformat() if completed_at else None,
            "duration": duration,
        })
        
    return sorted(executions, key=lambda x: x["started_at"] or "", reverse=True)


def get_dashboard_stats() -> dict[str, int]:
    """
    Calculate dashboard statistics from the event store.
    """
    executions = get_all_executions()
    
    running = sum(1 for e in executions if e["status"] == "RUNNING")
    completed_today = sum(1 for e in executions if e["status"] == "COMPLETED")  # simplified for demo
    failed_today = sum(1 for e in executions if e["status"] == "FAILED")
    
    return {
        "running": running,
        "completed_today": completed_today,
        "failed_today": failed_today,
        "plugins": 1  # Will be overridden by actual plugin registry count
    }
