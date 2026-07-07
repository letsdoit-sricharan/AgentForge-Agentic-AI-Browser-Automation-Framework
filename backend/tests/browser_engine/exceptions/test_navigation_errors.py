import asyncio

from app.browser_engine.exceptions.navigation_errors import NavigationError
from app.browser_engine.managers.browser_manager import BrowserManager
from app.browser_engine.models.browser_options import BrowserOptions


async def main():

    print("=" * 60)
    print("Navigation Error Test")
    print("=" * 60)

    manager = BrowserManager(
        BrowserOptions(headless=False)
    )

    await manager.start()

    session = await manager.create_session()

    page = await session.new_page()

    try:

        print("Opening invalid URL...")

        await page.goto("https://this-domain-does-not-exist-agentforge-123456789.com")

        print("❌ Navigation should have failed")

    except NavigationError as exc:

        print("✓ NavigationError raised")
        print(exc)

    finally:

        await session.close()
        await manager.stop()


if __name__ == "__main__":
    asyncio.run(main())