from app.browser_engine.exceptions.browser_errors import BrowserEngineError

class JavaScriptError(BrowserEngineError):
    """Base exception for JavaScript execution failures."""
    pass

class JavaScriptExecutionError(JavaScriptError):
    """Raised when the script throws a runtime exception inside the browser."""
    pass

class JavaScriptTimeoutError(JavaScriptError):
    """Raised when a script fails to resolve within the timeout."""
    pass

class JavaScriptSerializationError(JavaScriptError):
    """Raised when the return value cannot be serialized/deserialized."""
    pass
