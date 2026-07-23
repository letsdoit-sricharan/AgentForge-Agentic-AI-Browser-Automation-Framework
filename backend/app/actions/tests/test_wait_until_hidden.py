"""
Tests for WaitUntilHiddenAction.
"""

import asyncio

from app.actions.locator.wait_until_hidden import WaitUntilHiddenAction


class DummyLocator:

    async def wait_until_hidden(
        self,
        timeout=None,
    ):
        print(f"Waiting until hidden ({timeout} ms)")


class DummyPage:

    def locator(self, selector):
        print(f"Locate: {selector}")
        return DummyLocator()


async def run_test():

    print("\n==============================")
    print(" Wait Until Hidden Test ")
    print("==============================\n")

    page = DummyPage()

    action = WaitUntilHiddenAction(
        "#loading-spinner",
        timeout=5000,
    )

    await action.execute(page)

    print(f"✓ {action.name}")

    print("\n✅ Wait Until Hidden Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())
