"""
Tests for MoveMouseAction.
"""

import asyncio

from app.actions.mouse.move import MoveMouseAction


class DummyPage:

    async def move_mouse(
        self,
        x: float,
        y: float,
    ):
        print(f"Mouse moved to ({x}, {y})")


async def run_test():

    print("\n==============================")
    print(" Move Mouse Action Test ")
    print("==============================\n")

    page = DummyPage()

    action = MoveMouseAction(
        x=250,
        y=400,
    )

    await action.execute(page)

    print(f"✓ {action.name}")

    print("\n✅ Move Mouse Action Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())