"""
Tests for HotkeyAction.
"""

import asyncio

from app.actions.keyboard.hotkey import HotkeyAction


class DummyPage:

    async def hotkey(
        self,
        *keys: str,
    ):
        print(f"Hotkey: {' + '.join(keys)}")


async def run_test():

    print("\n==============================")
    print(" Hotkey Action Test ")
    print("==============================\n")

    page = DummyPage()

    action = HotkeyAction(
        keys=("Control", "A"),
    )

    await action.execute(page)

    print(f"✓ {action.name}")

    print("\n✅ Hotkey Action Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())