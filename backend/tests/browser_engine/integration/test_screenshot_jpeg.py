import asyncio
from pathlib import Path

from app.browser_engine.managers.browser_manager import BrowserManager
from app.browser_engine.models.browser_options import BrowserOptions
from app.browser_engine.models.screenshot_options import ScreenshotOptions
from app.browser_engine.models.screenshot_type import ScreenshotType


OUTPUT_DIR = Path("test_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


async def main():

    print("=" * 60)
    print("JPEG Screenshot Test")
    print("=" * 60)

    manager = BrowserManager(
        BrowserOptions(headless=False)
    )

    await manager.start()

    session = await manager.create_session()

    page = await session.new_page()

    await page.goto("https://www.google.com")

    options = ScreenshotOptions(
        path=OUTPUT_DIR / "google.jpg",
        image_type=ScreenshotType.JPEG,
        quality=80,
    )

    saved_path = await page.screenshot(options)

    assert saved_path.exists()
    assert saved_path.suffix == ".jpg"

    print("✓ JPEG screenshot created")

    await session.close()
    await manager.stop()


if __name__ == "__main__":
    asyncio.run(main())