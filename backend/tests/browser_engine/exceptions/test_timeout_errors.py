import asyncio

from app.browser_engine.exceptions.timeout_errors import BrowserTimeoutError
from app.browser_engine.managers.browser_manager import BrowserManager
from app.browser_engine.models.browser_options import BrowserOptions
from app.browser_engine.models.load_state import LoadState


async def main():

    print("=" * 60)
    print("Timeout Error Test")
    print("=" * 60)

    manager = BrowserManager(
        BrowserOptions(headless=False)
    )

    await manager.start()

    session = await manager.create_session()

    page = await session.new_page()

    print("Opening Google...")

    await page.goto("https://www.google.com")

    try:

        print("Waiting with impossible timeout...")

        await page.wait_for_load(
            state=LoadState.NETWORK_IDLE,
            timeout=1,
        )

        print("❌ Expected BrowserTimeoutError")

    except BrowserTimeoutError as exc:

        print("✓ BrowserTimeoutError raised")
        print(exc)

    finally:

        await session.close()
        await manager.stop()


if __name__ == "__main__":
    asyncio.run(main())