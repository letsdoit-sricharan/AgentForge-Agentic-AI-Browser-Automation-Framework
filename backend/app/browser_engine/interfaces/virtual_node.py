from dataclasses import dataclass, field
from typing import Any, Dict, Tuple


@dataclass
class VirtualNode:
    """
    Represents a virtual node (e.g., a shape or object) drawn on a non-DOM canvas interface.
    """
    id: str
    name: str
    type: str
    x: float
    y: float
    width: float
    height: float
    is_visible: bool = True
    attributes: Dict[str, Any] = field(default_factory=dict)

    @property
    def center(self) -> Tuple[float, float]:
        """
        Returns the absolute (x, y) center for native mouse interactions.
        Assumes x and y are the top-left coordinates of the bounding box relative to the viewport.
        """
        return self.x + (self.width / 2.0), self.y + (self.height / 2.0)
