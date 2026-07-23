import asyncio
from typing import Any, Type, TypeVar, Union

from playwright.async_api import Error as PlaywrightError
from playwright.async_api import Page as PlaywrightCorePage
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from pydantic import TypeAdapter, ValidationError

from app.browser_engine.javascript.bridge import JavaScriptBridge
from app.browser_engine.javascript.exceptions import (
    JavaScriptExecutionError,
    JavaScriptSerializationError,
    JavaScriptTimeoutError,
)

T = TypeVar("T")

class PlaywrightJavaScriptBridge(JavaScriptBridge):
    def __init__(self, page: PlaywrightCorePage):
        self._page = page

    async def evaluate(
        self,
        script: str,
        *args: Any,
        return_type: Type[T] = type(None),
        timeout: float = 30000.0
    ) -> Union[T, Any]:

        # We need a wrapper script if we want to enforce timeout natively in JS
        # But Playwright's evaluate doesn't take a timeout. We will use asyncio.wait_for
        try:
            raw_result = await asyncio.wait_for(
                self._page.evaluate(script, args if len(args) > 1 else (args[0] if args else None)),
                timeout=timeout / 1000.0
            )
        except asyncio.TimeoutError as e:
            raise JavaScriptTimeoutError(f"JavaScript execution timed out after {timeout}ms") from e
        except PlaywrightTimeoutError as e:
            raise JavaScriptTimeoutError(f"JavaScript execution timed out after {timeout}ms") from e
        except PlaywrightError as e:
            raise JavaScriptExecutionError(f"JavaScript execution failed: {str(e)}") from e
        except Exception as e:
            raise JavaScriptExecutionError(f"Unexpected error during JavaScript execution: {str(e)}") from e

        if return_type is type(None):
            return raw_result

        try:
            adapter = TypeAdapter(return_type)
            return adapter.validate_python(raw_result)
        except ValidationError as e:
            raise JavaScriptSerializationError(f"Failed to deserialize result to {return_type}: {str(e)}") from e
        except Exception as e:
            raise JavaScriptSerializationError(f"Unexpected serialization error: {str(e)}") from e

    async def add_script_tag(
        self,
        url: str | None = None,
        content: str | None = None
    ) -> None:
        try:
            await self._page.add_script_tag(url=url, content=content)
        except PlaywrightError as e:
            raise JavaScriptExecutionError(f"Failed to inject script tag: {str(e)}") from e
        except Exception as e:
            raise JavaScriptExecutionError(f"Unexpected error injecting script tag: {str(e)}") from e
