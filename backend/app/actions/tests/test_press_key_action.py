"""
Tests for PressKeyAction.
"""

import asyncio

from app.actions.keyboard.press_key import PressKeyAction


class DummyPage:

    async def press_key(
        self,
        key: str,
    ):
        print(f"Pressed: {key}")


async def run_test():

    print("\n==============================")
    print(" Press Key Action Test ")
    print("==============================\n")

    page = DummyPage()

    action = PressKeyAction("Enter")

    await action.execute(page)

    print(f"✓ {action.name}")

    print("\n✅ Press Key Action Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())