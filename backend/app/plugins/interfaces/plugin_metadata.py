"""
Purpose:
    Defines immutable metadata describing an AgentForge plugin.

Responsibilities:
    - Identify a plugin
    - Describe plugin capabilities
    - Provide plugin information to the registry and loader

Does NOT:
    - Execute plugins
    - Load plugins
    - Manage lifecycle
    - Access runtime or browser resources
"""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class PluginMetadata:
    """
    Immutable metadata describing a plugin.
    """

    name: str
    version: str
    description: str
    author: str
    capabilities: tuple[str, ...] = field(default_factory=tuple)
    homepage: str | None = None