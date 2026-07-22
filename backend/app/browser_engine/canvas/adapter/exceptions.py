from app.browser_engine.exceptions.browser_errors import BrowserEngineError

class CanvasAdapterError(BrowserEngineError):
    """Base exception for Canvas Adapter errors."""
    pass

class NodeMappingError(CanvasAdapterError):
    """Raised when a VirtualNodeMapper fails to translate raw JSON into a VirtualNode."""
    pass

class VirtualNodeNotFoundError(CanvasAdapterError):
    """Raised when a query yields no results but one was required."""
    pass
