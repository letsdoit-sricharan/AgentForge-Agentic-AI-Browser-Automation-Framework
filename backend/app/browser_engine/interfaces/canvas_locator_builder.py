"""
Purpose:
    Defines the abstract CanvasLocatorBuilder interface for the AgentForge Browser Engine.

Responsibilities:
    - Provide a fluent builder API for querying virtual nodes on a canvas element.
    - Delegate actual canvas traversal to a CanvasEngine implementation.

Must NOT do:
    - Import Playwright.
    - Contain implementation logic.
    - Handle logging, retries, or browser lifecycle.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from app.browser_engine.interfaces.virtual_node import VirtualNode


class CanvasLocatorBuilder(ABC):
    """
    Abstract fluent builder for locating virtual nodes within a canvas element.

    Usage example::

        node = await page.canvas("konva", "#stage").by_name("my-rect").first()
        nodes = await page.canvas("fabric", "#canvas").by_type("Circle").all()
    """

    @abstractmethod
    def by_name(self, name: str) -> "CanvasLocatorBuilder":
        """
        Filter virtual nodes by their ``name`` attribute.

        Args:
            name:
                The node name to match.

        Returns:
            This builder (for chaining).
        """
        raise NotImplementedError

    @abstractmethod
    def by_type(self, node_type: str) -> "CanvasLocatorBuilder":
        """
        Filter virtual nodes by their ``type`` attribute (e.g. ``"Rect"``, ``"Circle"``).

        Args:
            node_type:
                The node type string to match.

        Returns:
            This builder (for chaining).
        """
        raise NotImplementedError

    @abstractmethod
    def by_id(self, node_id: str) -> "CanvasLocatorBuilder":
        """
        Filter virtual nodes by their ``id`` attribute.

        Args:
            node_id:
                The node id to match.

        Returns:
            This builder (for chaining).
        """
        raise NotImplementedError

    @abstractmethod
    async def first(self) -> VirtualNode:
        """
        Resolve and return the first matching virtual node.

        Returns:
            The first matching :class:`VirtualNode`.

        Raises:
            LookupError:
                If no matching node is found.
        """
        raise NotImplementedError

    @abstractmethod
    async def all(self) -> List[VirtualNode]:
        """
        Resolve and return all matching virtual nodes.

        Returns:
            A list of matching :class:`VirtualNode` instances (may be empty).
        """
        raise NotImplementedError
