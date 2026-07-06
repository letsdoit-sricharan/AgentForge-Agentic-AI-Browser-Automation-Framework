import asyncio

from app.browser_engine.managers.browser_manager import BrowserManager
from app.browser_engine.models.browser_options import BrowserOptions


async def main():
    manager = BrowserManager(
        BrowserOptions(
            headless=False,
        )
    )

    print("=" * 60)
    print("Starting BrowserManager Test")
    print("=" * 60)

    print("Starting browser...")
    await manager.start()
    print("✓ Browser started")

    print("Creating session...")
    session = await manager.create_session()
    print("✓ Session created")

    print("Creating page...")
    page = await session.new_page()
    print("✓ Page created")

    print("Navigating to Google...")
    await page.goto("https://www.google.com")
    print("✓ Navigation successful")

    title = await page.title()
    print(f"Page title: {title}")

    print(f"Current URL: {page.url}")

    print("Closing session...")
    await session.close()
    print("✓ Session closed")

    print("Stopping browser...")
    await manager.stop()
    print("✓ Browser stopped")

    print("\nBrowserManager test completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())