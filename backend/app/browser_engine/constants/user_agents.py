"""
Purpose:
    Defines commonly used browser User-Agent strings.

Responsibilities:
    - Provide centralized user-agent definitions.
    - Avoid hardcoded strings throughout the Browser Engine.

Must NOT do:
    - Perform browser configuration.
    - Contain business logic.
"""

# Latest stable desktop Chrome (Windows)
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/138.0.0.0 Safari/537.36"
)

# Microsoft Edge
EDGE_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
)

# Firefox
FIREFOX_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) "
    "Gecko/20100101 Firefox/141.0"
)

# Safari (macOS)
SAFARI_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Version/18.0 Safari/605.1.15"
)