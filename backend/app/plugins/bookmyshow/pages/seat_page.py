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

import asyncio

from app.actions.element import ClickAction
from app.plugin_framework.pages import BasePage


class SeatPage(BasePage):
    """
    Page Object representing the seat selection page.
    """

    TICKET_COUNT_TEMPLATE = 'li[id="quantity-{}"]'

    SELECT_SEATS_BUTTON = "#select-seats-btn"

    PAY_BUTTON = "#pay-btn"

    async def select_ticket_count(self, count: int) -> None:
        """
        Select the number of tickets.
        """
        selector = self.TICKET_COUNT_TEMPLATE.format(count)

        count_locator = self.page.locator(selector)
        await count_locator.wait()
        await count_locator.click(force=True)

        btn_locator = self.page.locator(self.SELECT_SEATS_BUTTON)
        await btn_locator.wait(timeout=5000)
        await btn_locator.click(force=True)

    async def select_seats(self, count: int, preference: str | None = None) -> None:
        """
        Select available seats on the Konva canvas via JavaScript injection.

        Introspects the exposed ``window.__konvaStage`` to find all Rect nodes
        with name='Available', then simulates click events at their absolute
        coordinates using Playwright's mouse API.
        """
        await asyncio.sleep(0.5)

        # Ask Konva for the absolute positions of available seats via JS
        js_get_seats = """
        (function() {
            if (!window.__konvaStage) return [];
            var layer = window.__konvaStage.getLayers()[0];
            if (!layer) return [];
            return layer.getChildren(function(node) {
                return node.getAttr('name') === 'Available';
            }).map(function(node) {
                var pos = node.getAbsolutePosition();
                var width = node.width();
                var height = node.height();
                return {
                    x: pos.x + width / 2,
                    y: pos.y + height / 2
                };
            });
        })()
        """

        seats = await self.page.evaluate(js_get_seats)

        if not seats:
            # Fallback: click canvas at known seat positions (50+i*60+20, 120)
            canvas_locator = self.page.locator("canvas").first()
            bbox = await canvas_locator.bounding_box()
            if bbox:
                for i in range(count):
                    x = bbox["x"] + 70 + (i * 60)
                    y = bbox["y"] + 120
                    await self.page.mouse_click(x, y)
                    await asyncio.sleep(0.2)
            return

        for i in range(min(count, len(seats))):
            # Get canvas element bounding box to translate Konva coords -> page coords
            canvas_locator = self.page.locator("canvas").first()
            bbox = await canvas_locator.bounding_box()
            if bbox:
                page_x = bbox["x"] + seats[i]["x"]
                page_y = bbox["y"] + seats[i]["y"]
                await self.page.mouse_click(page_x, page_y)
                await asyncio.sleep(0.2)

    async def proceed_to_pay(self) -> None:
        """
        Click the Pay button.
        """
        pay_locator = self.page.locator(self.PAY_BUTTON).first()
        await pay_locator.wait(timeout=5000)
        await ClickAction(locator=pay_locator).execute(self.page)