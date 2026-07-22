"""
Purpose:
    Represents the BookMyShow theatre selection page.

Responsibilities:
    - Select a date.
    - Select a theatre.
    - Select a show time.
    - Handle any "Accept Terms" popups.

Does NOT:
    - Execute workflow logic.
    - Import Playwright.
"""

from __future__ import annotations

from app.actions.element import ClickAction
from app.plugin_framework.pages import BasePage


class TheatrePage(BasePage):
    """
    Page Object representing the theatre and show selection page.
    """

    DATE_FILTER_TEMPLATE = "text={}"

    THEATRE_NAME_TEMPLATE = "text={}"

    SHOW_TIME_TEMPLATE = "text={}"

    ACCEPT_TERMS_BUTTON = "text=Accept"

    async def select_date(self, show_date: str) -> None:
        """
        Select a specific date for the movie.
        """
        selector = self.DATE_FILTER_TEMPLATE.format(show_date)
        
        date_locator = self.page.locator(selector)
        await date_locator.wait()
        await ClickAction(locator=date_locator).execute(self.page)

    async def select_theatre_and_show(self, theatre: str, time: str) -> None:
        """
        Select a specific theatre and show time.
        """
        # Find the deepest div that contains both the theatre name and the show time,
        # then find the time element inside it.
        # This works correctly with BookMyShow's virtualized list structure.
        time_locator = (
            self.page.locator("div")
            .filter(has_text=theatre)
            .filter(has_text=time)
            .last()
            .locator(f'text="{time}"')
            .first()
        )
        
        await time_locator.wait()
        await ClickAction(locator=time_locator).execute(self.page)

    async def accept_terms(self) -> None:
        """
        Accept terms and conditions if the popup appears.
        """
        if not self.ACCEPT_TERMS_BUTTON:
            return
            
        try:
            terms_locator = self.page.locator(self.ACCEPT_TERMS_BUTTON)
            await terms_locator.wait(timeout=5000)
            if await terms_locator.is_visible():
                await ClickAction(locator=terms_locator).execute(self.page)
        except Exception:
            # Popup might not always appear
            pass