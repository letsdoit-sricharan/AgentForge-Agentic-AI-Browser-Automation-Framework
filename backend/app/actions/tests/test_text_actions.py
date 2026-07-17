"""
Tests for text input actions.
"""

import asyncio

from app.actions.element.fill import FillAction
from app.actions.element.clear import ClearAction


class DummyLocator:

    async def fill(self, text: str):
        print(f'Fill: "{text}"')

    async def clear(self):
        print("Clear")


class DummyPage:
    pass


async def run_test():

    print("\n==============================")
    print(" Text Actions Test ")
    print("==============================\n")

    locator = DummyLocator()
    page = DummyPage()

    actions = [
        FillAction(locator, "BookMyShow"),
        ClearAction(locator),
    ]

    for action in actions:
        await action.execute(page)
        print(f"✓ {action.name}")

    print("\n✅ Text Actions Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())