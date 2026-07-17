"""
Event handler interfaces.

Defines the contract implemented by all event handlers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.runtime.events.browser_event import BrowserEvent
from app.runtime.events.runtime_event import RuntimeEvent
from app.runtime.events.workflow_event import WorkflowEvent


class EventHandler(ABC):
    """
    Base interface for all event handlers.
    """

    @abstractmethod
    def handle(
        self,
        event: RuntimeEvent | BrowserEvent | WorkflowEvent,
    ) -> None:
        """
        Process an emitted event.
        """
        raise NotImplementedError