from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from app.browser_engine.canvas.adapter.exceptions import CanvasAdapterError
from app.browser_engine.canvas.adapter.mapper import VirtualNodeMapper
from app.browser_engine.canvas.adapter.query import VirtualNodeQuery
from app.browser_engine.javascript.bridge import JavaScriptBridge


class CanvasAdapter(ABC):
    """
    Orchestrates the fetching, mapping, and querying of virtual canvas nodes.
    Acts as the bridge between raw JavaScript renderer output and the Python Framework.
    """

    def __init__(self, js_bridge: JavaScriptBridge, mapper: VirtualNodeMapper):
        self._js_bridge = js_bridge
        self._mapper = mapper

    @abstractmethod
    async def fetch_raw_nodes(self, filter_hint: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Renderer-specific injection to fetch the raw scene graph.
        Subclasses (e.g., KonvaAdapter) must implement this to return a list
        of dictionaries representing the virtual nodes.

        Args:
            filter_hint: An optional string to allow the JS side to pre-filter
                         nodes for performance optimization on large graphs.

        Returns:
            A list of raw JSON dictionaries from the browser.
        """
        raise NotImplementedError

    async def get_nodes(self, filter_hint: Optional[str] = None) -> VirtualNodeQuery:
        """
        Fetches raw nodes, maps them to VirtualNodes, and returns a Query object
        for filtering natively in Python.
        """
        try:
            raw_nodes = await self.fetch_raw_nodes(filter_hint=filter_hint)
        except Exception as e:
            raise CanvasAdapterError(f"Failed to fetch raw nodes from JavaScript: {e}") from e

        mapped = []
        for raw_node in raw_nodes:
            mapped.append(self._mapper.map_node(raw_node))

        return VirtualNodeQuery(mapped)
