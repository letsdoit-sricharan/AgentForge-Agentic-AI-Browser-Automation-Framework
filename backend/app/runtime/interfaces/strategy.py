"""
Base strategy interface.

Runtime strategies encapsulate interchangeable policies
such as retry, wait, recovery, navigation, and timeout.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Strategy(ABC):
    """
    Base interface for runtime strategies.
    """

    @abstractmethod
    async def apply(self, *args: Any, **kwargs: Any) -> Any:
        """
        Apply the strategy.

        Returns:
            Any:
                Strategy-specific result.
        """
        raise NotImplementedError