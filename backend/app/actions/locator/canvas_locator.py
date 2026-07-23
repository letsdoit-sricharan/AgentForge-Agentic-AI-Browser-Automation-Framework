from typing import Optional
from app.browser_engine.interfaces.locator import Locator
from app.browser_engine.interfaces.page import Page
from app.browser_engine.canvas.adapter.canvas_adapter import CanvasAdapter


class CanvasLocatorBuilder:
    """Builder returned by page.canvas() to create CanvasLocators."""
    def __init__(self, page: Page, engine_type: str, dom_selector: str):
        self.page = page
        self.engine_type = engine_type
        self.dom_selector = dom_selector

    def locator(self, selector: str) -> "CanvasLocator":
        return CanvasLocator(self.page, self.dom_selector, self.engine_type, selector)


class CanvasLocator(Locator):
    """
    Locator for querying virtual canvas elements.
    Delegates to the specific CanvasEngine to resolve to absolute screen coordinates.
    """
    def __init__(self, page: Page, canvas_selector: str, engine_type: str, node_selector: str):
        self.page = page
        self.canvas_selector = canvas_selector
        self.engine_type = engine_type
        self.node_selector = node_selector

    async def _get_adapter(self) -> CanvasAdapter:
        if self.engine_type.lower() == "konva":
            from app.browser_engine.canvas.adapter.konva_adapter import KonvaAdapter
            return KonvaAdapter(self.page.js_bridge)
        raise ValueError(f"Unsupported canvas engine type: {self.engine_type}")

    async def _get_node(self):
        adapter = await self._get_adapter()
        query = await adapter.get_nodes()
        
        nth_val = None
        for part in self.node_selector.split("&"):
            part = part.strip()
            if "=" in part:
                k, v = part.split("=", 1)
                k = k.strip()
                v = v.strip()
                if k.lower() == "role":
                    query = query.by_role(v)
                elif k.lower() == "name":
                    query = query.by_text(v, exact=True)
                elif k.lower() == "nth":
                    nth_val = int(v)
                else:
                    query = query.by_attribute(k, v)
                    
        if nth_val is not None:
            from app.browser_engine.canvas.adapter.query import VirtualNodeQuery
            all_nodes = query.all()
            if 0 <= nth_val < len(all_nodes):
                query = VirtualNodeQuery([all_nodes[nth_val]])
            else:
                query = VirtualNodeQuery([])
                
        return query

    async def click(self, force: bool = False) -> None:
        nodes = await self._get_node()
        node = nodes.first()
        if not node:
            raise Exception(f"Canvas node not found for selector {self.node_selector}")
            
        # We need the absolute bounding box of the canvas DOM element itself to offset the virtual coordinates
        canvas_dom = self.page.locator(self.canvas_selector)
        bbox = await canvas_dom.bounding_box()
        if not bbox:
            raise Exception(f"Canvas DOM element '{self.canvas_selector}' has no bounding box.")
            
        # Click center of the virtual node, offset by the actual canvas DOM element position
        abs_x = bbox["x"] + node.x + (node.width / 2)
        abs_y = bbox["y"] + node.y + (node.height / 2)
        
        await self.page.mouse_click(abs_x, abs_y)

    async def count(self) -> int:
        nodes = await self._get_node()
        return len(nodes.all())

    async def get_attribute(self, name: str) -> str | None:
        nodes = await self._get_node()
        node = nodes.first()
        if not node:
            return None
        return str(node.attributes.get(name)) if name in node.attributes else None

    async def text_content(self) -> str | None:
        nodes = await self._get_node()
        node = nodes.first()
        if not node:
            return None
        return node.attributes.get("text")

    async def bounding_box(self) -> dict:
        nodes = await self._get_node()
        node = nodes.first()
        if not node:
            raise Exception("Node not found")
        return {"x": node.x, "y": node.y, "width": node.width, "height": node.height}

    async def is_visible(self) -> bool:
        nodes = await self._get_node()
        node = nodes.first()
        return node.is_visible if node else False
        
    async def fill(self, value: str) -> None:
        raise NotImplementedError
    async def text(self) -> str:
        return await self.text_content() or ""
    async def hover(self) -> None:
        raise NotImplementedError
    async def select(self, value: str) -> None:
        raise NotImplementedError
    async def wait(self, timeout: int | None = None) -> None:
        # In a real app we would poll, but for now we assume canvas renders synchronously
        pass
    def first(self) -> "Locator":
        return self
    def last(self) -> "Locator":
        return self
    def nth(self, index: int) -> "Locator":
        # Hacky support for nth: append it to the selector micro-syntax
        return CanvasLocator(self.page, self.canvas_selector, self.engine_type, f"{self.node_selector} & nth={index}")
    async def wait_until_hidden(self, timeout: int | None = None) -> None:
        pass
    async def scroll_into_view(self) -> None:
        pass
    def filter(self, has_text: str | None = None) -> "Locator":
        return self
    def locator(self, selector: str) -> "Locator":
        return CanvasLocator(self.page, self.canvas_selector, self.engine_type, selector)
