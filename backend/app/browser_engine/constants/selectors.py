"""
Purpose:
    Defines generic selector constants used by the Browser Engine.

Responsibilities:
    - Standardize selector strategy names.
    - Provide reusable selector prefixes.

Must NOT do:
    - Store website-specific selectors.
    - Contain BookMyShow, Amazon, or plugin selectors.
"""

# ---------------------------------------------------------------------------
# Selector Strategy Names
# ---------------------------------------------------------------------------

CSS = "css"
XPATH = "xpath"
TEXT = "text"
ROLE = "role"
TEST_ID = "test_id"
LABEL = "label"
PLACEHOLDER = "placeholder"

# ---------------------------------------------------------------------------
# Selector Prefixes
# ---------------------------------------------------------------------------

CSS_PREFIX = "css="
XPATH_PREFIX = "xpath="
TEXT_PREFIX = "text="

# ---------------------------------------------------------------------------
# Common HTML Selectors
# ---------------------------------------------------------------------------

BUTTON = "button"
INPUT = "input"
TEXTAREA = "textarea"
SELECT = "select"
FORM = "form"
LINK = "a"

# ---------------------------------------------------------------------------
# Common Attributes
# ---------------------------------------------------------------------------

DATA_TEST_ID = "data-testid"
ARIA_LABEL = "aria-label"
PLACEHOLDER_ATTR = "placeholder"
