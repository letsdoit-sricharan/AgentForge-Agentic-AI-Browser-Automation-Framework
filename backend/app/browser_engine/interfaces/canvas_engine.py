from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from app.browser_engine.interfaces.virtual_node import VirtualNode


class CanvasEngine(ABC):
    """
    Abstract interface for parsing and interacting with in-memory scene graphs.
    """

    @abstractmethod
    async def get_nodes(self, selector: str) -> List[VirtualNode]:
        """
        Executes JS in the browser context to traverse the scene graph
        and return nodes matching the query.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_node(self, selector: str) -> VirtualNode:
        """
        Returns the first matching virtual node.
        """
        raise NotImplementedError
