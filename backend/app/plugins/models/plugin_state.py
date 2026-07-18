"""
Purpose:
    Defines the lifecycle states of a plugin.

Responsibilities:
    - Represent plugin lifecycle.
    - Provide strongly typed plugin states.

Does NOT:
    - Manage state transitions.
    - Execute plugin logic.
"""

from enum import Enum


class PluginState(str, Enum):
    """
    Represents the lifecycle state of a plugin.
    """

    CREATED = "created"
    LOADED = "loaded"
    INITIALIZED = "initialized"
    RUNNING = "running"
    STOPPED = "stopped"
    FAILED = "failed"