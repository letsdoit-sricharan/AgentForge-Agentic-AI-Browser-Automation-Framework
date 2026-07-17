"""
Tests for ForwardAction.
"""

import asyncio

from app.actions.navigation.forward import ForwardAction


class DummyPage:
    """
    Fake Browser Engine page.
    """

    async def go_forward(self):
        print("Navigating Forward")


async def run_test():

    print("\n==============================")
    print(" Forward Action Test ")
    print("==============================\n")

    page = DummyPage()

    action = ForwardAction()

    await action.execute(page)

    print(f"Action Name : {action.name}")

    print("\n✅ Forward Action Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())