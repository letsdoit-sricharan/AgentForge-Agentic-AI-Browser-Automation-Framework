"""
Purpose:
    Define configuration options for launching browser instances and initializing contexts.

Responsibilities:
    - Hold parameters like headless mode, viewport settings, timeouts, and user agents.

Must NOT do:
    - Depend on any browser automation library or framework.
"""

from __future__ import annotations
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

from app.browser_engine.models.viewport import Viewport


class BrowserOptions(BaseModel):
    """
    Data model representing settings for launching and configuring a browser.
    """
    browser_name: str = Field(default="chromium", description="Browser type: chromium, firefox, webkit")
    headless: bool = Field(default=True, description="Run browser in headless mode")
    viewport: Optional[Viewport] = Field(default_factory=Viewport, description="Browser viewport settings")
    slow_mo: float = Field(default=0.0, description="Slow down interactions by given milliseconds")
    timeout: int = Field(default=30000, description="Default timeout in milliseconds")
    user_agent: Optional[str] = Field(default=None, description="Custom User-Agent string")
    proxy: Optional[Dict[str, str]] = Field(default=None, description="Proxy server configuration settings")
    args: List[str] = Field(default_factory=list, description="Additional command-line arguments to pass to the browser")
