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

    URL = "http://127.0.0.1:8000/demo/mock_bms.html"

    _NAV_TIMEOUT_MS = 60_000

    _LOAD_INDICATORS = [
        'input[placeholder*="Search"]',
        'input[aria-label*="Search"]',
    ]

    GLOBAL_SEARCH_BOX = '#search input[type="text"]'

    CITY_SEARCH_BOX = 'input[placeholder="Search for your city"]'

    CITY_RESULT_TEMPLATE = 'div[data-result-item="true"]:has-text("{}")'

    async def open(self) -> None:
        """
        Navigate to the BookMyShow homepage.
        """

        await NavigateAction(
            url=self.URL,
            options=NavigationOptions(
                wait_until=LoadState.DOM_CONTENT_LOADED,
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
            load_state=LoadState.DOM_CONTENT_LOADED,
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
                locator = self.page.locator(selector).first()

                await locator.wait(timeout=10_000)

                if await locator.is_visible():
                    return True

            except BrowserTimeoutError:
                continue

            except Exception:
                continue

        return False

    async def search_movie(
        self,
        movie_name: str,
    ) -> None:
        """
        Search for a movie.
        """

        search_button = self.page.locator(
            'div[aria-label^="Search for Movies"]',
        )

        await ClickAction(
            locator=search_button,
        ).execute(
            self.page,
        )

        search_box = self.page.locator(
            self.GLOBAL_SEARCH_BOX,
        )

        await FillAction(
            locator=search_box,
            text=movie_name,
        ).execute(
            self.page,
        )

    async def search_city(
        self,
        city: str,
    ) -> None:
        """
        Search for a city.
        """

        search_box = self.page.locator(
            self.CITY_SEARCH_BOX,
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

        selector = self.CITY_RESULT_TEMPLATE.format(city)

        city_locator = self.page.locator(
            selector,
        ).first()

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
            selector = 'text="{}"'.format(city)
            city_locator = self.page.locator(
                selector,
            ).first()

            return await city_locator.is_visible()

        except Exception:
            return False
