import asyncio

from app.browser_engine.managers.browser_manager import BrowserManager
from app.browser_engine.models.browser_options import BrowserOptions


async def open_page(
    session,
    url: str,
    page_name: str,
):
    """
    Open a page within an existing session.
    """

    page = await session.new_page()

    print(f"[{page_name}] Opening {url}")

    await page.goto(url)

    title = await page.title()

    print(f"[{page_name}] Title: {title}")

    print(f"[{page_name}] URL: {page.url}")

    return page


async def main():

    manager = BrowserManager(
        BrowserOptions(
            headless=False,
        )
    )

    print("=" * 60)
    print("Multiple Pages Test")
    print("=" * 60)

    print("Starting browser...")
    await manager.start()

    print("Creating one session...")
    session = await manager.create_session()

    print("Opening multiple pages...\n")

    pages = await asyncio.gather(
        open_page(
            session,
            "https://www.google.com",
            "Page-1",
        ),
        open_page(
            session,
            "https://github.com",
            "Page-2",
        ),
        open_page(
            session,
            "https://openai.com",
            "Page-3",
        ),
        open_page(
            session,
            "https://www.wikipedia.org",
            "Page-4",
        ),
    )

    print()

    print(f"Pages tracked by SessionManager: {session.page_count}")

    print(f"Active sessions: {manager.session_count}")

    print("\nClosing session...")

    await session.close()

    print("Session closed.")

    print(f"Pages after close: {session.page_count}")

    print(f"Active sessions: {manager.session_count}")

    await manager.stop()

    print()

    print("Browser stopped.")

    print("Multiple pages test completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())