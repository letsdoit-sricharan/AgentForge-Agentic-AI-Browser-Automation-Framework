"""
Tests for NavigateAction.
"""

import asyncio

from app.actions.navigation.navigate import NavigateAction


class DummyPage:
    """
    Fake Browser Engine page.
    """

    async def goto(
        self,
        url,
        options=None,
    ):
        print(f"Navigating to: {url}")


async def run_test():

    print("\n==============================")
    print(" Navigate Action Test ")
    print("==============================\n")

    page = DummyPage()

    action = NavigateAction(
        url="https://bookmyshow.com"
    )

    await action.execute(page)

    print(f"Action Name : {action.name}")
    print(f"URL         : {action.url}")

    print("\n✅ Navigate Action Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())