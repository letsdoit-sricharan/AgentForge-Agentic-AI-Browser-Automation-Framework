"""
Purpose:
    Represents the BookMyShow home page.

Responsibilities:
    - Open the homepage.
    - Wait until the homepage finishes loading.
    - Verify that the homepage is displayed.

Does NOT:
    - Execute workflow logic.
    - Import Playwright.
    - Contain business rules.
"""

from __future__ import annotations

from app.actions.navigation import NavigateAction, WaitAction
from app.browser_engine.models.load_state import LoadState
from app.plugin_framework.pages import BasePage


class HomePage(BasePage):
    """
    Page Object representing the BookMyShow homepage.
    """

    URL = "https://in.bookmyshow.com/explore/home"

    # Version 1.0
    # This selector should be reviewed periodically if the site changes.
    SEARCH_BOX = 'input[placeholder*="Search"]'

    async def open(self) -> None:
        """
        Navigate to the BookMyShow homepage.
        """

        await NavigateAction(
            url=self.URL,
        ).execute(
            self.page,
        )

    async def wait_until_loaded(self) -> None:
        """
        Wait until the homepage has finished loading.
        """

        await WaitAction(
            load_state=LoadState.LOAD,
        ).execute(
            self.page,
        )

    async def verify_loaded(self) -> bool:
        """
        Verify that the homepage has loaded successfully.
        """

        locator = self.page.locator(
            self.SEARCH_BOX,
        )

        await locator.wait()

        return await locator.is_visible()