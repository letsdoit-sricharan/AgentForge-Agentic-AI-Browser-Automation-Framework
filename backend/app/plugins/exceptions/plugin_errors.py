"""
Purpose:
    Defines exceptions for plugin operations.

Responsibilities:
    - Provide typed exceptions for plugin errors.
    - Enable granular error handling.
    - Support error diagnostics.

Does NOT:
    - Handle errors.
    - Log errors.
    - Manage plugin lifecycle.
"""


class PluginError(Exception):
    """Base exception for all plugin errors."""


class PluginNotFoundError(PluginError):
    """Raised when a plugin cannot be found."""

    def __init__(self, plugin_name: str) -> None:
        self.plugin_name = plugin_name
        super().__init__(f"Plugin not found: {plugin_name}")


class PluginAlreadyRegisteredError(PluginError):
    """Raised when attempting to register a duplicate plugin."""

    def __init__(self, plugin_name: str) -> None:
        self.plugin_name = plugin_name
        super().__init__(f"Plugin already registered: {plugin_name}")


class PluginLoadError(PluginError):
    """Raised when a plugin fails to load."""

    def __init__(self, plugin_name: str, reason: str) -> None:
        self.plugin_name = plugin_name
        self.reason = reason
        super().__init__(f"Failed to load plugin '{plugin_name}': {reason}")


class PluginInitializationError(PluginError):
    """Raised when a plugin fails to initialize."""

    def __init__(self, plugin_name: str, reason: str) -> None:
        self.plugin_name = plugin_name
        self.reason = reason
        super().__init__(f"Failed to initialize plugin '{plugin_name}': {reason}")


class PluginExecutionError(PluginError):
    """Raised when a plugin fails during execution."""

    def __init__(self, plugin_name: str, reason: str) -> None:
        self.plugin_name = plugin_name
        self.reason = reason
        super().__init__(f"Plugin execution failed '{plugin_name}': {reason}")


class PluginValidationError(PluginError):
    """Raised when plugin validation fails."""

    def __init__(self, plugin_name: str, errors: list[str]) -> None:
        self.plugin_name = plugin_name
        self.errors = errors
        error_list = "\n  - ".join(errors)
        super().__init__(f"Plugin validation failed for '{plugin_name}':\n  - {error_list}")


class PluginStateError(PluginError):
    """Raised when a plugin operation is invalid for current state."""

    def __init__(self, plugin_name: str, current_state: str, operation: str) -> None:
        self.plugin_name = plugin_name
        self.current_state = current_state
        self.operation = operation
        super().__init__(
            f"Cannot {operation} plugin '{plugin_name}' in state '{current_state}'"
        )


class PluginDependencyError(PluginError):
    """Raised when plugin dependencies are not satisfied."""

    def __init__(self, plugin_name: str, missing_dependencies: list[str]) -> None:
        self.plugin_name = plugin_name
        self.missing_dependencies = missing_dependencies
        deps = ", ".join(missing_dependencies)
        super().__init__(
            f"Plugin '{plugin_name}' has unsatisfied dependencies: {deps}"
        )
