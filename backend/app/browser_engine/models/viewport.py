"""
Purpose:
    Define the data model for the browser viewport dimensions and scaling settings.

Responsibilities:
    - Hold the width and height configurations of the browser window.
    - Hold mobile, landscape, and touch emulation settings.

Must NOT do:
    - Depend on any browser automation library or framework.
"""

from __future__ import annotations
from pydantic import BaseModel, Field


class Viewport(BaseModel):
    """
    Data model representing viewport dimensions and emulation properties.
    """
    width: int = Field(default=1280, description="Viewport width in pixels")
    height: int = Field(default=720, description="Viewport height in pixels")
    device_scale_factor: float = Field(default=1.0, description="Device scale factor / pixel ratio")
    is_mobile: bool = Field(default=False, description="Whether to emulate mobile device screen")
    has_touch: bool = Field(default=False, description="Whether to emulate touch events support")
    is_landscape: bool = Field(default=False, description="Whether viewport is landscape orientation")
