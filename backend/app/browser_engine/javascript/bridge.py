from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar, Union

T = TypeVar("T")

class JavaScriptBridge(ABC):
    """
    Browser-agnostic bridge for executing and injecting JavaScript.
    """

    @abstractmethod
    async def evaluate(
        self,
        script: str,
        *args: Any,
        return_type: Type[T] = type(None),
        timeout: float = 30000.0
    ) -> Union[T, Any]:
        """
        Executes JavaScript in the browser context.

        Args:
            script: The JavaScript function or expression to execute.
            args: Arguments to pass to the script.
            return_type: Optional type (e.g. Pydantic model or dataclass) to deserialize the result into.
            timeout: Execution timeout in milliseconds.

        Returns:
            The raw JSON result, or the deserialized `return_type` instance.

        Raises:
            JavaScriptExecutionError: If the script throws a runtime exception.
            JavaScriptTimeoutError: If the script fails to resolve within the timeout.
            JavaScriptSerializationError: If the return value cannot be serialized/deserialized.
        """
        raise NotImplementedError

    @abstractmethod
    async def add_script_tag(
        self, 
        url: str | None = None, 
        content: str | None = None
    ) -> None:
        """
        Injects a `<script>` tag into the page. Useful for loading external libraries 
        or injecting large, reusable client-side functions.
        
        Must provide either `url` or `content`.
        """
        raise NotImplementedError
