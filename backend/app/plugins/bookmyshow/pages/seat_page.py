"""
Purpose:
    Represents the BookMyShow seat selection page.

Responsibilities:
    - Select ticket count.
    - Select specific seats.
    - Click Pay button.

Does NOT:
    - Execute workflow logic.
    - Import Playwright.
"""

from __future__ import annotations

from app.actions.element import ClickAction
from app.plugin_framework.pages import BasePage


class SeatPage(BasePage):
    """
    Page Object representing the seat selection page.
    """

    TICKET_COUNT_TEMPLATE = 'li[id="quantity-{}"]'
    
    SELECT_SEATS_BUTTON = "role=button[name='Select Seats'i]"

    AVAILABLE_SEAT_TEMPLATE = "role=button[name='Available'i]"

    PAY_BUTTON = "role=button[name=/Pay/i]"

    async def select_ticket_count(self, count: int) -> None:
        """
        Select the number of tickets.
        """
        selector = self.TICKET_COUNT_TEMPLATE.format(count)
        
        count_locator = self.page.locator(selector)
        await count_locator.wait()
        await count_locator.click(force=True)

        btn_locator = self.page.locator(self.SELECT_SEATS_BUTTON)
        await btn_locator.click(force=True)

    async def select_seats(self, count: int, preference: str | None = None) -> None:
        """
        Select available seats on the map using the Canvas Engine.
        """
        # Create a canvas locator builder for Konva using the canvas DOM selector
        canvas_builder = self.page.canvas("konva", "canvas")
        
        # We assume available seats have some identifier like name="Available" in Konva
        # The micro-syntax in CanvasLocator supports this
        available_seats = canvas_builder.locator("name=Available")
        
        for i in range(count):
            # nth() returns a new CanvasLocator targeting the i-th element
            seat_locator = available_seats.nth(i)
            # click() will resolve the node and dispatch mouse events at absolute coordinates
            await seat_locator.click(force=True)

    async def proceed_to_pay(self) -> None:
        """
        Click the Pay button.
        """
        pay_locator = self.page.locator(self.PAY_BUTTON)
        await pay_locator.wait()
        await ClickAction(locator=pay_locator).execute(self.page)