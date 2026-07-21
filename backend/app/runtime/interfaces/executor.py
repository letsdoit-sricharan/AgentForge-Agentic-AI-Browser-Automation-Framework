"""
Base executor interface.

All runtime executors should implement this contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Executor(ABC):
    """
    Base interface for all runtime executors.
    """

    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        """
        Execute a unit of work.

        Returns:
            Any:
                Result produced by the executor.
        """
        raise NotImplementedError
