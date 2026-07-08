"""
Event bus interface.

Defines the contract for runtime event publication
and subscription.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class EventBus(ABC):
    """
    Base event bus interface.
    """

    @abstractmethod
    def subscribe(
        self,
        event_type: str,
        handler: Callable[..., Any],
    ) -> None:
        """
        Register an event handler.
        """
        raise NotImplementedError

    @abstractmethod
    def unsubscribe(
        self,
        event_type: str,
        handler: Callable[..., Any],
    ) -> None:
        """
        Remove an event handler.
        """
        raise NotImplementedError

    @abstractmethod
    async def publish(
        self,
        event: Any,
    ) -> None:
        """
        Publish an event.
        """
        raise NotImplementedError