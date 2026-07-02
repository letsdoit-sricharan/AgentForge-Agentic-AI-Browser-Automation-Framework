"""
Purpose:
    Define configuration settings for capturing screenshots.

Responsibilities:
    - Hold parameters like screenshot path, format, quality, and full-page capture options.

Must NOT do:
    - Depend on any browser automation library or framework.
"""

from __future__ import annotations
from typing import Optional, List
from pydantic import BaseModel, Field


class ScreenshotOptions(BaseModel):
    """
    Data model representing settings for taking page and element screenshots.
    """
    path: Optional[str] = Field(default=None, description="Output file path where screenshot is saved")
    full_page: bool = Field(default=False, description="Capture full scrollable page screenshot")
    type: str = Field(default="png", description="Image format: 'png' or 'jpeg'")
    quality: Optional[int] = Field(default=None, description="Quality for jpeg format (0-100)")
    omit_background: bool = Field(default=False, description="Hide default background to support transparent images")
    mask: Optional[List[str]] = Field(default=None, description="CSS selectors to mask before taking screenshot")
    timeout: float = Field(default=30000.0, description="Timeout in milliseconds for capturing screenshot")
