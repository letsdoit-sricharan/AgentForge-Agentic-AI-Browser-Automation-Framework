import asyncio

from app.browser_engine.managers.browser_manager import BrowserManager
from app.browser_engine.models.browser_options import BrowserOptions


async def main():

    manager = BrowserManager(
        BrowserOptions(headless=False)
    )

    print("=" * 60)
    print("Locator Hover Test")
    print("=" * 60)

    await manager.start()

    session = await manager.create_session()

    page = await session.new_page()

    print("Opening hover page...")

    await page.goto(
        "https://the-internet.herokuapp.com/hovers"
    )

    image = page.locator(".figure").first()

    print("Waiting for image...")

    await image.wait()

    print("Image visible:", await image.is_visible())

    print("Hovering over image...")

    await image.hover()

    caption = page.locator(".figcaption").first()

    await caption.wait()

    print("Caption visible:", await caption.is_visible())

    text = await caption.text()

    print()

    print("Caption text:")

    print(text.strip())

    await session.close()

    await manager.stop()

    print()

    print("Hover test completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())