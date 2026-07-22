from typing import List

from app.browser_engine.interfaces.canvas_engine import CanvasEngine
from app.browser_engine.interfaces.page import Page
from app.browser_engine.interfaces.virtual_node import VirtualNode


class FabricEngine(CanvasEngine):
    """
    CanvasEngine implementation for FabricJS.
    """
    def __init__(self, page: Page, canvas_selector: str):
        self.page = page
        self.canvas_selector = canvas_selector

    async def get_nodes(self, selector: str) -> List[VirtualNode]:
        raise NotImplementedError

    async def get_node(self, selector: str) -> VirtualNode:
        raise NotImplementedError
