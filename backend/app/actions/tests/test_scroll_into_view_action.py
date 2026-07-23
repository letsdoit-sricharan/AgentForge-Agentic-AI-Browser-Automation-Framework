"""
Tests for ScrollIntoViewAction.
"""

import asyncio

from app.actions.page.scroll_into_view import ScrollIntoViewAction


class DummyLocator:

    async def scroll_into_view(self):
        print("Element scrolled into view")


class DummyPage:
    pass


async def run_test():

    print("\n==============================")
    print(" Scroll Into View Action Test ")
    print("==============================\n")

    page = DummyPage()

    locator = DummyLocator()

    action = ScrollIntoViewAction(locator)

    await action.execute(page)

    print(f"✓ {action.name}")

    print("\n✅ Scroll Into View Action Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())
