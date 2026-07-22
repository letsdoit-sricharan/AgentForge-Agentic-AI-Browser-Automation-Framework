from typing import Any, Dict, List, Optional
from app.browser_engine.canvas.adapter.canvas_adapter import CanvasAdapter
from app.browser_engine.canvas.adapter.mapper import VirtualNodeMapper
from app.browser_engine.interfaces.virtual_node import VirtualNode
from app.browser_engine.canvas.adapter.exceptions import NodeMappingError
from app.browser_engine.javascript.bridge import JavaScriptBridge


class KonvaNodeMapper(VirtualNodeMapper):
    def map_node(self, raw_data: Dict[str, Any]) -> VirtualNode:
        try:
            return VirtualNode(
                id=raw_data.get("id", ""),
                name=raw_data.get("name", ""),
                type=raw_data.get("className", ""),
                x=float(raw_data.get("x", 0)),
                y=float(raw_data.get("y", 0)),
                width=float(raw_data.get("width", 0)),
                height=float(raw_data.get("height", 0)),
                is_visible=bool(raw_data.get("visible", True)),
                attributes=raw_data.get("attrs", {})
            )
        except (ValueError, TypeError) as e:
            raise NodeMappingError(f"Failed to map raw data to VirtualNode: {e}") from e


class KonvaAdapter(CanvasAdapter):
    """
    Konva-specific CanvasAdapter.
    Injects JS to extract the Konva scene graph.
    """

    def __init__(self, js_bridge: JavaScriptBridge):
        super().__init__(js_bridge, KonvaNodeMapper())

    async def fetch_raw_nodes(self, filter_hint: Optional[str] = None) -> List[Dict[str, Any]]:
        script = """
        () => {
            if (typeof window.Konva === 'undefined' || !window.Konva.stages) {
                return [];
            }
            
            const nodes = [];
            
            function traverse(node) {
                if (!node) return;
                
                const absPos = node.getAbsolutePosition();
                const size = node.size ? node.size() : {width: 0, height: 0};
                
                nodes.push({
                    id: node.id() || "",
                    name: node.name() || "",
                    className: node.getClassName() || "",
                    x: absPos.x || 0,
                    y: absPos.y || 0,
                    width: size.width || 0,
                    height: size.height || 0,
                    visible: node.isVisible(),
                    attrs: node.attrs || {}
                });
                
                if (node.children) {
                    node.children.forEach(traverse);
                }
            }
            
            window.Konva.stages.forEach(traverse);
            return nodes;
        }
        """
        
        result = await self._js_bridge.evaluate(script)
        if not isinstance(result, list):
            return []
        return result
