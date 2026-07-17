"""
Tests for WaitForElementAction.
"""

import asyncio

from app.actions.locator.wait_for_element import WaitForElementAction


class DummyLocator:

    async def wait(self, timeout=None):
        print(f"Waiting ({timeout} ms)")


class DummyPage:

    def locator(self, selector):
        print(f"Locate: {selector}")
        return DummyLocator()


async def run_test():

    print("\n==============================")
    print(" Wait For Element Test ")
    print("==============================\n")

    page = DummyPage()

    action = WaitForElementAction(
        "#login-button",
        timeout=5000,
    )

    locator = await action.execute(page)

    assert locator is not None

    print(f"✓ {action.name}")

    print("\n✅ Wait For Element Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())