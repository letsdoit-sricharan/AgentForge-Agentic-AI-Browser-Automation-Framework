import pytest
from typing import Any, Dict, List, Optional
from unittest.mock import AsyncMock

from app.browser_engine.interfaces.virtual_node import VirtualNode
from app.browser_engine.canvas.adapter.mapper import VirtualNodeMapper
from app.browser_engine.canvas.adapter.query import VirtualNodeQuery
from app.browser_engine.canvas.adapter.canvas_adapter import CanvasAdapter
from app.browser_engine.javascript.bridge import JavaScriptBridge

# Mock Mapper
class MockMapper(VirtualNodeMapper):
    def map_node(self, raw_data: Dict[str, Any]) -> VirtualNode:
        return VirtualNode(
            id=raw_data.get("id", ""),
            name=raw_data.get("name", ""),
            type=raw_data.get("type", "Rect"),
            x=raw_data.get("x", 0.0),
            y=raw_data.get("y", 0.0),
            width=raw_data.get("width", 10.0),
            height=raw_data.get("height", 10.0),
            is_visible=raw_data.get("visible", True),
            attributes=raw_data
        )

# Concrete Adapter for testing
class DummyCanvasAdapter(CanvasAdapter):
    async def fetch_raw_nodes(self, filter_hint: Optional[str] = None) -> List[Dict[str, Any]]:
        # Mocking JS bridge call
        result = await self._js_bridge.evaluate("return dummy_nodes;")
        return result

@pytest.fixture
def dummy_nodes():
    return [
        {"id": "node1", "name": "Seat A1", "type": "Rect", "x": 10, "y": 10, "visible": True, "category": "VIP"},
        {"id": "node2", "name": "Seat A2", "type": "Rect", "x": 30, "y": 10, "visible": False, "category": "Regular"},
        {"id": "node3", "name": "Label1", "type": "Text", "x": 10, "y": 50, "visible": True, "text": "Screen"}
    ]

@pytest.fixture
def js_bridge(dummy_nodes):
    bridge = AsyncMock(spec=JavaScriptBridge)
    bridge.evaluate.return_value = dummy_nodes
    return bridge

@pytest.fixture
def adapter(js_bridge):
    mapper = MockMapper()
    return DummyCanvasAdapter(js_bridge, mapper)

@pytest.mark.asyncio
async def test_adapter_fetches_and_maps(adapter):
    query = await adapter.get_nodes()
    
    assert isinstance(query, VirtualNodeQuery)
    nodes = query.all()
    assert len(nodes) == 3
    assert nodes[0].id == "node1"
    assert nodes[2].type == "Text"

def test_query_by_attribute():
    mapper = MockMapper()
    nodes = [
        mapper.map_node({"id": "1", "status": "available"}),
        mapper.map_node({"id": "2", "status": "booked"}),
    ]
    
    query = VirtualNodeQuery(nodes)
    result = query.by_attribute("status", "available").all()
    
    assert len(result) == 1
    assert result[0].id == "1"

def test_query_chaining():
    mapper = MockMapper()
    nodes = [
        mapper.map_node({"id": "1", "visible": True, "type": "Rect"}),
        mapper.map_node({"id": "2", "visible": False, "type": "Rect"}),
        mapper.map_node({"id": "3", "visible": True, "type": "Circle"}),
    ]
    
    query = VirtualNodeQuery(nodes)
    result = query.is_visible().by_role("Rect").first()
    
    assert result is not None
    assert result.id == "1"

def test_query_in_bounds():
    mapper = MockMapper()
    nodes = [
        mapper.map_node({"id": "1", "x": 10, "y": 10, "width": 10, "height": 10}),
        mapper.map_node({"id": "2", "x": 50, "y": 50, "width": 10, "height": 10}),
    ]
    
    query = VirtualNodeQuery(nodes)
    result = query.in_bounds(0, 0, 30, 30).all()
    
    assert len(result) == 1
    assert result[0].id == "1"

def test_query_by_text():
    mapper = MockMapper()
    nodes = [
        mapper.map_node({"id": "1", "text": "Hello World"}),
        mapper.map_node({"id": "2", "name": "ExactMatch"}),
    ]
    
    query = VirtualNodeQuery(nodes)
    
    # Substring match
    res1 = query.by_text("World").all()
    assert len(res1) == 1
    assert res1[0].id == "1"
    
    # Exact match on name
    res2 = query.by_text("ExactMatch", exact=True).all()
    assert len(res2) == 1
    assert res2[0].id == "2"
