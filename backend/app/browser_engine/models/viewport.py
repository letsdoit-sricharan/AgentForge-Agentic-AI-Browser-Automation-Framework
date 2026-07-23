"""
Purpose:
    Defines the Viewport model used by the AgentForge Browser Engine.

Responsibilities:
    - Represent browser viewport dimensions.
    - Validate viewport configuration.
    - Provide a reusable, strongly typed configuration object.

Must NOT do:
    - Import Playwright.
    - Contain browser logic.
    - Resize browser windows.
    - Handle configuration loading.
"""

from pydantic import BaseModel, ConfigDict, Field


class Viewport(BaseModel):
    """
    Represents the dimensions of a browser viewport.

    This model is browser-agnostic and can be translated into
    browser-specific viewport settings by the implementation layer.
    """

    model_config = ConfigDict(frozen=True)

    width: int = Field(
        default=1280,
        gt=0,
        description="Viewport width in pixels."
    )

    height: int = Field(
        default=720,
        gt=0,
        description="Viewport height in pixels."
    )
