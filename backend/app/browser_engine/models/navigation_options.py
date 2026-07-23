"""
Purpose:
    Defines navigation configuration for page navigation operations.

Responsibilities:
    - Store browser-agnostic navigation settings.
    - Validate navigation configuration.
    - Provide a reusable configuration model.

Must NOT do:
    - Import Playwright.
    - Perform navigation.
    - Contain browser logic.
"""

from pydantic import BaseModel, ConfigDict, Field

from app.browser_engine.models.load_state import LoadState


class NavigationOptions(BaseModel):
    """
    Configuration options used during page navigation.
    """

    model_config = ConfigDict(frozen=True)

    timeout: int = Field(
        default=30_000,
        ge=0,
        description="Maximum navigation timeout in milliseconds.",
    )

    wait_until: LoadState = Field(
        default=LoadState.LOAD,
        description="Page load state that marks navigation as complete.",
    )
