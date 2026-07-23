"""
Tests for FindAction.
"""

import asyncio

from app.actions.locator.find import FindAction


class DummyLocator:
    pass


class DummyPage:

    def locator(self, selector: str):
        print(f"Locate: {selector}")
        return DummyLocator()


async def run_test():

    print("\n==============================")
    print(" Find Action Test ")
    print("==============================\n")

    page = DummyPage()

    action = FindAction("#movie-search")

    locator = await action.execute(page)

    assert isinstance(locator, DummyLocator)

    print(f"✓ {action.name}")

    print("\n✅ Find Action Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())
