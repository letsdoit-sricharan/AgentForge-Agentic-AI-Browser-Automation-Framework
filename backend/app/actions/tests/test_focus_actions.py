"""
Tests for focus actions.
"""

import asyncio

from app.actions.element.focus import FocusAction
from app.actions.element.blur import BlurAction


class DummyLocator:

    async def focus(self):
        print("Focus")

    async def blur(self):
        print("Blur")


class DummyPage:
    pass


async def run_test():

    print("\n==============================")
    print(" Focus Actions Test ")
    print("==============================\n")

    locator = DummyLocator()
    page = DummyPage()

    actions = [
        FocusAction(locator),
        BlurAction(locator),
    ]

    for action in actions:
        await action.execute(page)
        print(f"✓ {action.name}")

    print("\n✅ Focus Actions Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())