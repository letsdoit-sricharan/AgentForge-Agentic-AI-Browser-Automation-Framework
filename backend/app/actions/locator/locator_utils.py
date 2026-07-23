"""
Locator utilities.

Provides reusable helper functions for
locator-related actions.
"""

from __future__ import annotations


def validate_selector(selector: str) -> str:
    """
    Validate a locator selector.

    Args:
        selector:
            CSS, XPath, text, or other supported selector.

    Returns:
        The validated selector.

    Raises:
        ValueError:
            If the selector is invalid.
    """

    selector = selector.strip()

    if not selector:
        raise ValueError(
            "Selector cannot be empty."
        )

    return selector
