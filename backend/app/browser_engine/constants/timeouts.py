"""
Purpose:
    Defines default timeout values used throughout the Browser Engine.

Responsibilities:
    - Centralize timeout configuration.
    - Eliminate magic numbers.
    - Provide consistent defaults across browser operations.

Must NOT do:
    - Contain business logic.
    - Import Playwright.
    - Store plugin-specific configuration.
"""

# ---------------------------------------------------------------------------
# Browser Lifecycle
# ---------------------------------------------------------------------------

DEFAULT_BROWSER_LAUNCH_TIMEOUT = 30_000
DEFAULT_BROWSER_CLOSE_TIMEOUT = 10_000

# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------

DEFAULT_NAVIGATION_TIMEOUT = 30_000
DEFAULT_PAGE_LOAD_TIMEOUT = 30_000

# ---------------------------------------------------------------------------
# Elements
# ---------------------------------------------------------------------------

DEFAULT_ELEMENT_TIMEOUT = 10_000
DEFAULT_CLICK_TIMEOUT = 10_000
DEFAULT_FILL_TIMEOUT = 10_000

# ---------------------------------------------------------------------------
# Downloads
# ---------------------------------------------------------------------------

DEFAULT_DOWNLOAD_TIMEOUT = 60_000

# ---------------------------------------------------------------------------
# Screenshots
# ---------------------------------------------------------------------------

DEFAULT_SCREENSHOT_TIMEOUT = 15_000

# ---------------------------------------------------------------------------
# Polling / Retry
# ---------------------------------------------------------------------------

DEFAULT_POLL_INTERVAL = 500
DEFAULT_RETRY_COUNT = 3
