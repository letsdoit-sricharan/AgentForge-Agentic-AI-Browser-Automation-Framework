"""
Purpose:
    Represents the BookMyShow home page.

Responsibilities:
    - Open the homepage.
    - Wait until the homepage finishes loading.
    - Verify that the homepage is displayed.
    - Search and select a city.

Does NOT:
    - Execute workflow logic.
    - Import Playwright.
    - Contain business rules.
"""

from __future__ import annotations

from app.actions.element import ClickAction, FillAction
from app.actions.navigation import NavigateAction, WaitAction
from app.browser_engine.exceptions.timeout_errors import BrowserTimeoutError
from app.browser_engine.models.load_state import LoadState
from app.browser_engine.models.navigation_options import NavigationOptions
from app.plugin_framework.pages import BasePage


class HomePage(BasePage):
    """
    Page Object representing the BookMyShow homepage.
    """

    URL = "https://in.bookmyshow.com/explore/home"

    _NAV_TIMEOUT_MS = 60_000

    _LOAD_INDICATORS = [
        'input[placeholder*="Search"]',
        'input[aria-label*="Search"]',
        'input[type="search"]',
        'header',
        'nav',
    ]

    SEARCH_BOX = 'input[placeholder="Search for your city"]'

    async def open(self) -> None:
        """
        Navigate to the BookMyShow homepage.
        """

        await NavigateAction(
            url=self.URL,
            options=NavigationOptions(
                wait_until=LoadState.NETWORK_IDLE,
                timeout=self._NAV_TIMEOUT_MS,
            ),
        ).execute(
            self.page,
        )

    async def wait_until_loaded(self) -> None:
        """
        Wait until the homepage finishes loading.
        """

        await WaitAction(
            load_state=LoadState.NETWORK_IDLE,
            timeout=self._NAV_TIMEOUT_MS,
        ).execute(
            self.page,
        )

    async def verify_loaded(self) -> bool:
        """
        Verify the homepage has loaded.
        """

        for selector in self._LOAD_INDICATORS:

            try:
                locator = self.page.locator(selector)

                await locator.wait(timeout=10_000)

                if await locator.is_visible():
                    return True

            except BrowserTimeoutError:
                continue

            except Exception:
                continue

        return False

    async def search_city(
        self,
        city: str,
    ) -> None:
        """
        Search for a city.
        """

        search_box = self.page.locator(
            self.SEARCH_BOX,
        )

        await FillAction(
            locator=search_box,
            text=city,
        ).execute(
            self.page,
        )

    async def select_city(
        self,
        city: str,
    ) -> None:
        """
        Select the requested city.
        """

        city_locator = self.page.locator(
            f"text={city}",
        )

        await city_locator.wait()

        await ClickAction(
            locator=city_locator,
        ).execute(
            self.page,
        )

    async def verify_city_selected(
        self,
        city: str,
    ) -> bool:
        """
        Verify that the city selection succeeded.
        """

        try:
            city_locator = self.page.locator(
                f"text={city}",
            )

            return await city_locator.is_visible()

        except Exception:
            return False