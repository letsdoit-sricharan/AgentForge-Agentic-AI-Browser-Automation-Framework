"""
Purpose:
    Define helper formats, prefixes, and selector types used by the Browser Engine.

Responsibilities:
    - Hold common prefix types for DOM querying (CSS, XPath, Text).

Must NOT do:
    - Contain domain-specific selectors or target-website-specific paths.
"""

from __future__ import annotations

# Selector strategies prefix
CSS_PREFIX: str = "css="
XPATH_PREFIX: str = "xpath="
TEXT_PREFIX: str = "text="
ID_PREFIX: str = "id="
