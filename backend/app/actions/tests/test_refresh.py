"""
Tests for RefreshAction.
"""

import asyncio

from app.actions.navigation.refresh import RefreshAction


class DummyPage:
    """
    Fake Browser Engine page.
    """

    async def reload(self):
        print("Refreshing Page")


async def run_test():

    print("\n==============================")
    print(" Refresh Action Test ")
    print("==============================\n")

    page = DummyPage()

    action = RefreshAction()

    await action.execute(page)

    print(f"Action Name : {action.name}")

    print("\n✅ Refresh Action Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())