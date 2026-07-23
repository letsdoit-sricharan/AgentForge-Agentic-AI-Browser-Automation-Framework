"""
Tests for ScreenshotAction.
"""

import asyncio
from pathlib import Path

from app.actions.page.screenshot import ScreenshotAction
from app.browser_engine.models.screenshot_options import ScreenshotOptions


class DummyPage:

    async def screenshot(
        self,
        options: ScreenshotOptions,
    ) -> Path:

        print(f"Saving screenshot to {options.path}")

        return options.path


async def run_test():

    print("\n==============================")
    print(" Screenshot Action Test ")
    print("==============================\n")

    page = DummyPage()

    options = ScreenshotOptions(
        path=Path("screenshots/test.png"),
    )

    action = ScreenshotAction(options)

    path = await action.execute(page)

    print(path)

    print(f"✓ {action.name}")

    print("\n✅ Screenshot Action Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())
