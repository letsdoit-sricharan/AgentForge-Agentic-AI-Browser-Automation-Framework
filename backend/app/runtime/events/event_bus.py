"""
Event bus.

Provides publish/subscribe functionality for runtime events.
"""

from __future__ import annotations

from app.runtime.events.browser_event import BrowserEvent
from app.runtime.events.event_handlers import EventHandler
from app.runtime.events.runtime_event import RuntimeEvent
from app.runtime.events.workflow_event import WorkflowEvent


Event = RuntimeEvent | BrowserEvent | WorkflowEvent


class EventBus:
    """
    Central dispatcher for runtime events.
    """

    def __init__(self) -> None:
        self._handlers: list[EventHandler] = []

    def subscribe(
        self,
        handler: EventHandler,
    ) -> None:
        """
        Register an event handler.
        """
        if handler not in self._handlers:
            self._handlers.append(handler)

    def unsubscribe(
        self,
        handler: EventHandler,
    ) -> None:
        """
        Remove an event handler.
        """
        if handler in self._handlers:
            self._handlers.remove(handler)

    def publish(
        self,
        event: Event,
    ) -> None:
        """
        Publish an event to all registered handlers.
        """
        for handler in self._handlers:
            handler.handle(event)

    def clear(self) -> None:
        """
        Remove all registered handlers.
        """
        self._handlers.clear()

    @property
    def handler_count(self) -> int:
        """
        Number of subscribed handlers.
        """
        return len(self._handlers)

    @property
    def has_handlers(self) -> bool:
        """
        Returns True if at least one handler is registered.
        """
        return len(self._handlers) > 0