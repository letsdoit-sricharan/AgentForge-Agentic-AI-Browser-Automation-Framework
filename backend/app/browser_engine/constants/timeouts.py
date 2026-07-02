"""
Purpose:
    Define default timeout durations used by the Browser Engine.

Responsibilities:
    - Hold standard millisecond-based timeout durations for actions, loads, and connections.

Must NOT do:
    - Contain dynamic logic or variables.
"""

from __future__ import annotations

# Standard timeout durations in milliseconds
DEFAULT_TIMEOUT_MS: int = 30000
NAVIGATION_TIMEOUT_MS: int = 30000
SHORT_TIMEOUT_MS: int = 5000
LONG_TIMEOUT_MS: int = 60000
RESOURCE_LOAD_TIMEOUT_MS: int = 15000
