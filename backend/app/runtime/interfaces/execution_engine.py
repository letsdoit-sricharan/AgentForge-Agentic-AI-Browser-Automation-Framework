"""
Execution engine interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ExecutionEngine(ABC):
    """
    Contract for runtime execution engines.
    """

    @abstractmethod
    async def start(self, *args: Any, **kwargs: Any) -> Any:
        """
        Start a new execution.
        """
        raise NotImplementedError

    @abstractmethod
    async def pause(
        self,
        execution_id: str,
    ) -> None:
        """
        Pause an active execution.
        """
        raise NotImplementedError

    @abstractmethod
    async def resume(
        self,
        execution_id: str,
    ) -> None:
        """
        Resume a paused execution.
        """
        raise NotImplementedError

    @abstractmethod
    async def cancel(
        self,
        execution_id: str,
    ) -> None:
        """
        Cancel an execution.
        """
        raise NotImplementedError