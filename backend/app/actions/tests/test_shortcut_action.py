"""
Tests for ShortcutAction.
"""

import asyncio

from app.actions.keyboard.shortcut import ShortcutAction


class DummyPage:

    async def hotkey(
        self,
        *keys: str,
    ):
        print(f"Shortcut: {' + '.join(keys)}")


async def run_test():

    print("\n==============================")
    print(" Shortcut Action Test ")
    print("==============================\n")

    page = DummyPage()

    action = ShortcutAction("copy")

    await action.execute(page)

    print(f"✓ {action.name}")

    print("\n✅ Shortcut Action Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())
