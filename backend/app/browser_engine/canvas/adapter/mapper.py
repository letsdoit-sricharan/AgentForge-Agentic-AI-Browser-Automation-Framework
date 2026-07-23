from abc import ABC, abstractmethod
from typing import Any, Dict

from app.browser_engine.interfaces.virtual_node import VirtualNode


class VirtualNodeMapper(ABC):
    """
    Translates a renderer-specific raw JSON dictionary into a standardized VirtualNode.
    """
    @abstractmethod
    def map_node(self, raw_data: Dict[str, Any]) -> VirtualNode:
        """
        Map a raw dictionary to a VirtualNode.

        Args:
            raw_data: The raw JSON dictionary returned by the JavaScript bridge.

        Returns:
            A VirtualNode instance.

        Raises:
            NodeMappingError: If the raw data is missing required fields or has invalid types.
        """
        raise NotImplementedError
