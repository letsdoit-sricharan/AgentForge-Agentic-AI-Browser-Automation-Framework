from typing import List

from app.browser_engine.interfaces.canvas_engine import CanvasEngine
from app.browser_engine.interfaces.virtual_node import VirtualNode
from app.browser_engine.canvas.adapter.canvas_adapter import CanvasAdapter


class KonvaEngine(CanvasEngine):
    """
    CanvasEngine implementation for KonvaJS.
    """
    def __init__(self, adapter: CanvasAdapter):
        self._adapter = adapter

    async def get_nodes(self, selector: str) -> List[VirtualNode]:
        """
        Executes JS in the browser context to traverse the scene graph
        and return nodes matching the query.
        """
        # A selector here could be treated as a filter_hint, or we pull all and filter.
        # For simplicity, we delegate to adapter.
        query = await self._adapter.get_nodes(filter_hint=selector)
        return query.all()

    async def get_node(self, selector: str) -> VirtualNode:
        """
        Returns the first matching virtual node.
        """
        query = await self._adapter.get_nodes(filter_hint=selector)
        node = query.first()
        if not node:
            raise ValueError(f"No node found for selector: {selector}")
        return node
