"""
Tests for BackAction.
"""

import asyncio

from app.actions.navigation.back import BackAction


class DummyPage:
    """
    Fake Browser Engine page.
    """

    async def go_back(self):
        print("Navigating Back")


async def run_test():

    print("\n==============================")
    print(" Back Action Test ")
    print("==============================\n")

    page = DummyPage()

    action = BackAction()

    await action.execute(page)

    print(f"Action Name : {action.name}")

    print("\n✅ Back Action Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())