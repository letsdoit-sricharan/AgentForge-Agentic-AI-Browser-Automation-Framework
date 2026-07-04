"""
Purpose:
    Defines supported screenshot image formats for the AgentForge Browser Engine.

Responsibilities:
    - Represent supported screenshot formats.
    - Provide a browser-agnostic abstraction for image types.

Must NOT do:
    - Import Playwright.
    - Capture screenshots.
    - Perform file operations.
"""

from enum import Enum


class ScreenshotType(str, Enum):
    """
    Supported screenshot image formats.
    """

    PNG = "png"
    JPEG = "jpeg"