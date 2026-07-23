"""
Purpose:
    Defines the base abstraction for BookMyShow page locators.

Responsibilities:
    - Provide a common interface for page locator definitions.
    - Expose the page URL where applicable.

Does NOT:
    - Perform browser automation.
    - Execute actions.
    - Contain Playwright code.
"""

from __future__ import annotations

from abc import ABC
from typing import ClassVar


class PageLocators(ABC):
    """
    Base class for all BookMyShow page locator definitions.
    """

    URL: ClassVar[str] = ""
