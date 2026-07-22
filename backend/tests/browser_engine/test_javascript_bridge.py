import pytest
from pydantic import BaseModel

from app.browser_engine.javascript.exceptions import (
    JavaScriptExecutionError,
    JavaScriptSerializationError,
    JavaScriptTimeoutError,
)

from unittest.mock import AsyncMock, MagicMock
from playwright.async_api import Error as PlaywrightError
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

class PersonModel(BaseModel):
    name: str
    age: int

@pytest.fixture
def mock_core_page():
    page = AsyncMock()
    
    # Default behavior for evaluate
    async def mock_evaluate(script, args=None):
        if "hello" in script: return "hello"
        if "42" in script: return 42
        if "true" in script: return True
        if "a * 2" in script: return args * 2
        if "Alice" in script and "invalid_age" not in script:
            return {"name": "Alice", "age": 30}
        if "invalid_age" in script:
            return {"name": "Alice", "age": "invalid_age"}
        if "throw new Error" in script:
            raise PlaywrightError("Test JS Error")
        if "Promise" in script:
            raise PlaywrightTimeoutError("Timeout")
        if "TEST_INJECTION" in script:
            return 99
        return None
        
    page.evaluate.side_effect = mock_evaluate
    
    # Default behavior for add_script_tag
    async def mock_add_script_tag(url=None, content=None):
        pass
    
    page.add_script_tag.side_effect = mock_add_script_tag
    return page

@pytest.fixture
def page(mock_core_page):
    from app.browser_engine.implementations.playwright.playwright_javascript_bridge import PlaywrightJavaScriptBridge
    
    class DummyWrapper:
        def __init__(self, core_page):
            self.js_bridge = PlaywrightJavaScriptBridge(core_page)
            
    return DummyWrapper(mock_core_page)

@pytest.mark.asyncio
async def test_evaluate_primitives(page):
    js_bridge = page.js_bridge
    
    result_str = await js_bridge.evaluate("() => 'hello'")
    assert result_str == "hello"
    
    result_int = await js_bridge.evaluate("() => 42")
    assert result_int == 42
    
    result_bool = await js_bridge.evaluate("() => true")
    assert result_bool is True

@pytest.mark.asyncio
async def test_evaluate_with_args(page):
    js_bridge = page.js_bridge
    
    result = await js_bridge.evaluate("(a) => a * 2", 21)
    assert result == 42

@pytest.mark.asyncio
async def test_evaluate_typed_models(page):
    js_bridge = page.js_bridge
    
    script = "() => ({ name: 'Alice', age: 30 })"
    
    person = await js_bridge.evaluate(script, return_type=PersonModel)
    
    assert isinstance(person, PersonModel)
    assert person.name == 'Alice'
    assert person.age == 30

@pytest.mark.asyncio
async def test_evaluate_serialization_error(page):
    js_bridge = page.js_bridge
    
    script = "() => ({ name: 'Alice', age: 'invalid_age' })"
    
    with pytest.raises(JavaScriptSerializationError):
        await js_bridge.evaluate(script, return_type=PersonModel)

@pytest.mark.asyncio
async def test_evaluate_execution_error(page):
    js_bridge = page.js_bridge
    
    script = "() => { throw new Error('Test JS Error'); }"
    
    with pytest.raises(JavaScriptExecutionError):
        await js_bridge.evaluate(script)

@pytest.mark.asyncio
async def test_evaluate_timeout_error(page):
    js_bridge = page.js_bridge
    
    # A promise that never resolves
    script = "() => new Promise(() => {})"
    
    with pytest.raises(JavaScriptTimeoutError):
        await js_bridge.evaluate(script, timeout=10) # very short timeout

@pytest.mark.asyncio
async def test_add_script_tag(page):
    js_bridge = page.js_bridge
    
    # Inject a simple script that sets a global variable
    await js_bridge.add_script_tag(content="window.TEST_INJECTION = 99;")
    
    result = await js_bridge.evaluate("() => window.TEST_INJECTION")
    assert result == 99
