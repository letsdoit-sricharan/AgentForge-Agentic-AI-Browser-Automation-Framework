"""
Purpose:
    Define default user agents for the browser contexts.

Responsibilities:
    - Hold desktop and mobile user agent strings to help emulate real browsers.

Must NOT do:
    - Include logic for rotation or fetching remote agent lists.
"""

from __future__ import annotations

DEFAULT_DESKTOP_UA: str = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/114.0.0.0 Safari/537.36"
)

DEFAULT_MOBILE_UA: str = (
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/114.0.0.0 Mobile Safari/537.36"
)
