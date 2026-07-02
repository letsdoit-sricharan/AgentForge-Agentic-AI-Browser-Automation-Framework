"""
Purpose:
    Provide utilities for formatting, serializing, and validating cookies.

Responsibilities:
    - Serialize cookies to JSON structure.
    - Validate cookie attributes before loading into context.

Must NOT do:
    - Deal directly with file I/O operations (delegated to managers or paths).
"""

from __future__ import annotations
from typing import Any, Dict, List


def format_cookies_for_storage(cookies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Format and clean cookie dictionaries to ensure they are safe for serialization.
    """
    cleaned_cookies = []
    for cookie in cookies:
        cleaned_cookie = {
            "name": cookie.get("name"),
            "value": cookie.get("value"),
            "domain": cookie.get("domain"),
            "path": cookie.get("path", "/"),
            "expires": cookie.get("expires"),
            "httpOnly": cookie.get("httpOnly", False),
            "secure": cookie.get("secure", False),
            "sameSite": cookie.get("sameSite", "Lax"),
        }
        # Only include non-None properties
        cleaned_cookies.append({k: v for k, v in cleaned_cookie.items() if v is not None})
    return cleaned_cookies
