import asyncio

from app.browser_engine.exceptions.browser_errors import LocatorError
from app.browser_engine.managers.browser_manager import BrowserManager
from app.browser_engine.models.browser_options import BrowserOptions


async def main():

    print("=" * 60)
    print("Locator Error Test")
    print("=" * 60)

    manager = BrowserManager(
        BrowserOptions(headless=False)
    )

    await manager.start()

    session = await manager.create_session()

    page = await session.new_page()

    print("Opening page...")

    await page.goto("https://the-internet.herokuapp.com/login")

    try:

        print("Creating invalid locator...")

        invalid = page.locator("#this-element-does-not-exist")

        print("Attempting click...")

        await invalid.click()

        print("❌ Expected LocatorError")

    except LocatorError as exc:

        print("✓ LocatorError raised")
        print(exc)

    finally:

        await session.close()
        await manager.stop()


if __name__ == "__main__":
    asyncio.run(main())