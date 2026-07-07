import asyncio

from app.browser_engine.exceptions.browser_errors import PageError
from app.browser_engine.managers.browser_manager import BrowserManager
from app.browser_engine.models.browser_options import BrowserOptions


async def main():

    print("=" * 60)
    print("Page Error Test")
    print("=" * 60)

    manager = BrowserManager(
        BrowserOptions(headless=False)
    )

    await manager.start()

    session = await manager.create_session()

    page = await session.new_page()

    print("Opening Google...")

    await page.goto("https://www.google.com")

    print("Closing page...")

    await page.close()

    try:

        print("Attempting to get page title after close...")

        await page.title()

        print("❌ Expected PageError")

    except PageError as exc:

        print("✓ PageError raised")
        print(exc)

    finally:

        await session.close()
        await manager.stop()


if __name__ == "__main__":
    asyncio.run(main())