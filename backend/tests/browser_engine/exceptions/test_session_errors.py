import asyncio

from app.browser_engine.exceptions.browser_errors import SessionError
from app.browser_engine.managers.browser_manager import BrowserManager
from app.browser_engine.models.browser_options import BrowserOptions


async def main():

    print("=" * 60)
    print("Session Error Test")
    print("=" * 60)

    manager = BrowserManager(
        BrowserOptions(headless=False)
    )

    await manager.start()

    session = await manager.create_session()

    print("Closing session...")

    await session.close()

    try:

        print("Creating page after session is closed...")

        await session.new_page()

        print("❌ Expected SessionError")

    except SessionError as exc:

        print("✓ SessionError raised")
        print(exc)

    finally:

        await manager.stop()


if __name__ == "__main__":
    asyncio.run(main())