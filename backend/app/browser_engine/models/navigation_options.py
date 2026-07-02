"""
Purpose:
    Define configuration settings for page navigations.

Responsibilities:
    - Hold parameters like navigation timeouts, referer, and page-load waiting strategy.

Must NOT do:
    - Depend on any browser automation library or framework.
"""

from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


class NavigationOptions(BaseModel):
    """
    Data model representing options for page navigation and waiting events.
    """
    timeout: float = Field(default=30000.0, description="Max navigation duration in milliseconds")
    wait_until: str = Field(
        default="load",
        description="Event indicating completion: 'load', 'domcontentloaded', 'networkidle', 'commit'"
    )
    referer: Optional[str] = Field(default=None, description="Referer header value for navigation request")
