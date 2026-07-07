import asyncio
from pathlib import Path

from app.browser_engine.managers.browser_manager import BrowserManager
from app.browser_engine.models.browser_options import BrowserOptions
from app.browser_engine.models.screenshot_options import ScreenshotOptions


OUTPUT_DIR = Path("test_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


async def main():

    print("=" * 60)
    print("Full Page Screenshot Test")
    print("=" * 60)

    manager = BrowserManager(
        BrowserOptions(headless=False)
    )

    await manager.start()

    session = await manager.create_session()

    page = await session.new_page()

    await page.goto("https://en.wikipedia.org/wiki/Main_Page")

    options = ScreenshotOptions(
        path=OUTPUT_DIR / "wikipedia_full.png",
        full_page=True,
    )

    saved_path = await page.screenshot(options)

    assert saved_path.exists()

    print("✓ Full page screenshot captured")

    await session.close()
    await manager.stop()


if __name__ == "__main__":
    asyncio.run(main())