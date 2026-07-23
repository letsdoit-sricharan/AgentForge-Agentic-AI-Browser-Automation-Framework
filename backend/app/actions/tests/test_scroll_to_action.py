"""
Tests for ScrollToAction.
"""

import asyncio

from app.actions.page.scroll_to import ScrollToAction


class DummyPage:

    async def scroll_to(
        self,
        x: float,
        y: float,
    ):
        print(f"Scrolled to ({x}, {y})")


async def run_test():

    print("\n==============================")
    print(" Scroll To Action Test ")
    print("==============================\n")

    page = DummyPage()

    action = ScrollToAction(
        x=0,
        y=1500,
    )

    await action.execute(page)

    print(f"✓ {action.name}")

    print("\n✅ Scroll To Action Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())
