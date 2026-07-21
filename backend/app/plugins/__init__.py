"""
AgentForge Plugin System

The plugin system provides a framework-agnostic architecture for building
browser automation plugins that can be dynamically loaded, registered, and executed.

Architecture:
    - Plugin: Base interface for all plugins
    - PluginContext: Controlled execution context provided to plugins
    - PluginMetadata: Immutable plugin descriptors
    - PluginLoader: Dynamic module loading and instantiation
    - PluginRegistry: Central registration and lookup
    - PluginManager: Orchestrates lifecycle management
    - PluginState: Tracks runtime state and transitions

Key Principles:
    - Browser Independence: Plugins never import Playwright
    - Clean Architecture: Clear separation of concerns
    - Dependency Inversion: Plugins depend on abstractions
    - Framework Agnostic: Plugins work with any browser engine
"""

from app.plugins.exceptions import (
    PluginAlreadyRegisteredError,
    PluginDependencyError,
    PluginError,
    PluginExecutionError,
    PluginInitializationError,
    PluginLoadError,
    PluginNotFoundError,
    PluginStateError,
    PluginValidationError,
)
from app.plugins.interfaces import (
    Plugin,
    PluginContext,
    PluginMetadata,
)
from app.plugins.manager import (
    PluginLoader,
    PluginManager,
)
from app.plugins.models import (
    ManagedPlugin,
    PluginState,
    PluginStatus,
)
from app.plugins.registry import PluginRegistry

__all__ = [
    # Interfaces
    "Plugin",
    "PluginContext",
    "PluginMetadata",
    # Manager
    "PluginManager",
    "PluginLoader",
    # Registry
    "PluginRegistry",
    # Models
    "PluginState",
    "PluginStatus",
    "ManagedPlugin",
    # Exceptions
    "PluginError",
    "PluginNotFoundError",
    "PluginLoadError",
    "PluginInitializationError",
    "PluginExecutionError",
    "PluginAlreadyRegisteredError",
    "PluginDependencyError",
    "PluginValidationError",
    "PluginStateError",
]
