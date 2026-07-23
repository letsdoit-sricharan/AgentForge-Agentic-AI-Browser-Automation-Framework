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
    print("Locator Integration Test")
    print("=" * 60)

    await manager.start()

    session = await manager.create_session()

    page = await session.new_page()

    print("Opening login page...")

    await page.goto(
        "https://the-internet.herokuapp.com/login"
    )

    print("Creating locators...")

    username = page.locator("#username")
    password = page.locator("#password")
    login = page.locator("button[type='submit']")
    flash = page.locator("#flash")

    print("Waiting for username field...")

    await username.wait()

    print("Checking visibility...")

    print(
        "Username visible:",
        await username.is_visible(),
    )

    print(
        "Password visible:",
        await password.is_visible(),
    )

    print("Filling username...")

    await username.fill("tomsmith")

    print("Filling password...")

    await password.fill("SuperSecretPassword!")

    print("Clicking login...")

    await login.click()

    print("Waiting for message...")

    await flash.wait()

    text = await flash.text()

    print()

    print("Returned message:")

    print(text.strip())

    await session.close()

    await manager.stop()

    print()

    print("Locator test completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())