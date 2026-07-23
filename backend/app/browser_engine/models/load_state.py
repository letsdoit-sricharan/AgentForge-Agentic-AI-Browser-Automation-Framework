"""
Purpose:
    Defines browser-agnostic page load states for the AgentForge Browser Engine.

Responsibilities:
    - Represent page load completion states.
    - Provide a browser-independent abstraction.
    - Be translated into browser-specific values by implementation layers.

Must NOT do:
    - Import Playwright.
    - Contain browser logic.
    - Perform navigation.
"""

from enum import Enum


class LoadState(str, Enum):
    """
    Represents the page load state used by the Browser Engine.

    Concrete browser implementations are responsible for translating
    these values into the equivalent browser-specific load states.
    """

    LOAD = "load"
    DOM_CONTENT_LOADED = "domcontentloaded"
    NETWORK_IDLE = "networkidle"
