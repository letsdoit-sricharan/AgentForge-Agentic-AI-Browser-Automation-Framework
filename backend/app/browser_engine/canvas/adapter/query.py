from __future__ import annotations
from typing import Any, Callable, List

from app.browser_engine.interfaces.virtual_node import VirtualNode


class VirtualNodeQuery:
    """
    A fluent query and filtering system for VirtualNode collections.
    """

    def __init__(self, nodes: List[VirtualNode]):
        self._nodes = nodes

    def by_attribute(self, key: str, value: Any) -> "VirtualNodeQuery":
        """Filter nodes that have a specific attribute equal to the given value."""
        filtered = [n for n in self._nodes if n.attributes.get(key) == value]
        return VirtualNodeQuery(filtered)

    def by_text(self, text: str, exact: bool = False) -> "VirtualNodeQuery":
        """Filter nodes based on text. For now maps to 'text' attribute or node name."""
        def match(n: VirtualNode) -> bool:
            node_text = n.attributes.get("text", "") or n.name
            if not isinstance(node_text, str):
                return False
            return text == node_text if exact else text in node_text

        return VirtualNodeQuery([n for n in self._nodes if match(n)])

    def by_role(self, role: str) -> "VirtualNodeQuery":
        """Filter nodes by their logical role/type."""
        return VirtualNodeQuery([n for n in self._nodes if n.type == role])

    def is_visible(self) -> "VirtualNodeQuery":
        """Filter only visible nodes."""
        return VirtualNodeQuery([n for n in self._nodes if n.is_visible])

    def in_bounds(self, x: float, y: float, w: float, h: float) -> "VirtualNodeQuery":
        """Filter nodes that fall entirely within the specified bounding box."""
        def match(n: VirtualNode) -> bool:
            return (
                n.x >= x and
                n.y >= y and
                (n.x + n.width) <= (x + w) and
                (n.y + n.height) <= (y + h)
            )
        return VirtualNodeQuery([n for n in self._nodes if match(n)])

    def custom_filter(self, predicate: Callable[[VirtualNode], bool]) -> "VirtualNodeQuery":
        """Filter nodes using a custom python predicate."""
        return VirtualNodeQuery([n for n in self._nodes if predicate(n)])

    def all(self) -> List[VirtualNode]:
        """Return all matching nodes."""
        return self._nodes

    def first(self) -> VirtualNode | None:
        """Return the first matching node, or None if the query yields no results."""
        return self._nodes[0] if self._nodes else None
