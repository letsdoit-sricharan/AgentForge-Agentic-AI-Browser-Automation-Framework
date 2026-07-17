"""
Tests for mouse interaction actions.
"""

import asyncio

from app.actions.element.click import ClickAction
from app.actions.element.double_click import DoubleClickAction
from app.actions.element.right_click import RightClickAction
from app.actions.element.hover import HoverAction


class DummyLocator:

    async def click(self):
        print("Click")

    async def double_click(self):
        print("Double Click")

    async def right_click(self):
        print("Right Click")

    async def hover(self):
        print("Hover")


class DummyPage:
    pass


async def run_test():

    print("\n==============================")
    print(" Mouse Element Actions Test ")
    print("==============================\n")

    locator = DummyLocator()
    page = DummyPage()

    actions = [
        ClickAction(locator),
        DoubleClickAction(locator),
        RightClickAction(locator),
        HoverAction(locator),
    ]

    for action in actions:
        await action.execute(page)
        print(f"✓ {action.name}")

    print("\n✅ Mouse Element Actions Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())