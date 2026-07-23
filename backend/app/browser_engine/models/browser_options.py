"""
Purpose:
    Defines the BrowserOptions model for configuring browser instances.

Responsibilities:
    - Store browser launch configuration.
    - Validate browser configuration values.
    - Provide a reusable, browser-agnostic configuration object.

Must NOT do:
    - Import Playwright.
    - Launch browsers.
    - Read configuration from environment variables.
    - Contain browser logic.
"""

from pathlib import Path
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.browser_engine.models.viewport import Viewport


class BrowserOptions(BaseModel):
    """
    Configuration options used when launching a browser instance.

    This model is browser-agnostic and is translated into
    browser-specific launch options by the implementation layer.
    """

    model_config = ConfigDict(frozen=True)

    headless: bool = Field(
        default=True,
        description="Launch the browser in headless mode.",
    )

    viewport: Viewport = Field(
        default_factory=Viewport,
        description="Browser viewport configuration.",
    )

    user_agent: Optional[str] = Field(
        default=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        description="Optional custom browser user agent.",
    )

    slow_mo: int = Field(
        default=0,
        ge=0,
        description="Delay between browser actions in milliseconds.",
    )

    downloads_path: Optional[Path] = Field(
        default=None,
        description="Directory where browser downloads are stored.",
    )
