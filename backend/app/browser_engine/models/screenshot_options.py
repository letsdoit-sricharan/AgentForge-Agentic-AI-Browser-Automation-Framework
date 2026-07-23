"""
Purpose:
    Defines screenshot configuration for the AgentForge Browser Engine.

Responsibilities:
    - Store screenshot configuration.
    - Validate screenshot settings.
    - Provide a reusable browser-agnostic configuration object.

Must NOT do:
    - Import Playwright.
    - Capture screenshots.
    - Perform file operations.
    - Contain browser logic.
"""

from pathlib import Path
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.browser_engine.models.screenshot_type import ScreenshotType


class ScreenshotOptions(BaseModel):
    """
    Configuration options used when capturing a screenshot.

    This model is browser-agnostic and is translated into
    browser-specific screenshot options by the implementation layer.
    """

    model_config = ConfigDict(frozen=True)

    path: Path = Field(
        description="Destination path where the screenshot will be saved."
    )

    full_page: bool = Field(
        default=False,
        description="Capture the entire page instead of only the visible viewport.",
    )

    image_type: ScreenshotType = Field(
        default=ScreenshotType.PNG,
        description="Image format used for the screenshot.",
    )

    quality: Optional[int] = Field(
        default=None,
        ge=0,
        le=100,
        description="JPEG image quality (0-100). Applicable only for JPEG screenshots.",
    )

    @model_validator(mode="after")
    def validate_quality(self) -> "ScreenshotOptions":
        """
        Ensure that quality is only specified for JPEG screenshots.
        """

        if self.image_type == ScreenshotType.PNG and self.quality is not None:
            raise ValueError(
                "Quality can only be specified when image_type is JPEG."
            )

        return self
