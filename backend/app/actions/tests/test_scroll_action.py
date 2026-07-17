"""
Tests for ScrollAction.
"""

import asyncio

from app.actions.page.scroll import ScrollAction


class DummyPage:

    async def scroll(
        self,
        delta_x: float = 0,
        delta_y: float = 0,
    ):
        print(
            f"Scrolling page "
            f"(delta_x={delta_x}, delta_y={delta_y})"
        )


async def run_test():

    print("\n==============================")
    print(" Scroll Action Test ")
    print("==============================\n")

    page = DummyPage()

    action = ScrollAction(
        delta_y=800,
    )

    await action.execute(page)

    print(f"✓ {action.name}")

    print("\n✅ Scroll Action Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())