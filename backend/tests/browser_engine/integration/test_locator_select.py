import asyncio

from app.browser_engine.managers.browser_manager import BrowserManager
from app.browser_engine.models.browser_options import BrowserOptions


async def main():

    manager = BrowserManager(
        BrowserOptions(headless=False)
    )

    print("=" * 60)
    print("Locator Select Test")
    print("=" * 60)

    await manager.start()

    session = await manager.create_session()

    page = await session.new_page()

    print("Opening dropdown page...")

    await page.goto(
        "https://the-internet.herokuapp.com/dropdown"
    )

    dropdown = page.locator("#dropdown")

    await dropdown.wait()

    print("Dropdown visible:", await dropdown.is_visible())

    print("Selecting Option 2...")

    await dropdown.select("2")

    print("Option selected successfully.")

    await session.close()

    await manager.stop()

    print()

    print("Select test completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())