import asyncio

from app.browser_engine.exceptions.browser_errors import BrowserClosedError
from app.browser_engine.managers.browser_manager import BrowserManager
from app.browser_engine.models.browser_options import BrowserOptions


async def main():

    print("=" * 60)
    print("Browser Error Test")
    print("=" * 60)

    manager = BrowserManager(
        BrowserOptions(headless=False)
    )

    print("Starting browser...")
    await manager.start()

    print("Stopping browser...")
    await manager.stop()

    try:

        print("Creating session after browser stopped...")

        await manager.create_session()

        print("❌ Expected BrowserError")

    except BrowserClosedError as exc:

        print("✓ BrowserError raised")
        print(exc)


if __name__ == "__main__":
    asyncio.run(main())