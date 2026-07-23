"""
Tests for form actions.
"""

import asyncio

from app.actions.element.check import CheckAction
from app.actions.element.select_option import SelectOptionAction
from app.actions.element.uncheck import UncheckAction


class DummyLocator:

    async def check(self):
        print("Check")

    async def uncheck(self):
        print("Uncheck")

    async def select_option(self, value: str):
        print(f'Select option: "{value}"')


class DummyPage:
    pass


async def run_test():

    print("\n==============================")
    print(" Form Actions Test ")
    print("==============================\n")

    locator = DummyLocator()
    page = DummyPage()

    actions = [
        CheckAction(locator),
        UncheckAction(locator),
        SelectOptionAction(locator, "IMAX"),
    ]

    for action in actions:
        await action.execute(page)
        print(f"✓ {action.name}")

    print("\n✅ Form Actions Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())
