import asyncio

from app.browser_engine.managers.browser_manager import BrowserManager
from app.browser_engine.models.browser_options import BrowserOptions


async def visit_site(
    browser_manager: BrowserManager,
    url: str,
    name: str,
) -> None:
    """
    Create an independent browser session,
    visit a website, print its title,
    then clean up the session.
    """

    session = await browser_manager.create_session()

    page = await session.new_page()

    print(f"[{name}] Opening {url}")

    await page.goto(url)

    title = await page.title()

    print(f"[{name}] Title: {title}")

    print(f"[{name}] URL: {page.url}")

    await session.close()

    print(f"[{name}] Session closed")


async def main():

    manager = BrowserManager(
        BrowserOptions(
            headless=False,
        )
    )

    print("=" * 60)
    print("Multiple Session Test")
    print("=" * 60)

    await manager.start()

    await asyncio.gather(
        visit_site(
            manager,
            "https://www.google.com",
            "Session-1",
        ),
        visit_site(
            manager,
            "https://github.com",
            "Session-2",
        ),
        visit_site(
            manager,
            "https://openai.com",
            "Session-3",
        ),
    )

    print()

    print(
        f"Active sessions tracked: {manager.session_count}"
    )

    await manager.stop()

    print()

    print("Browser stopped.")

    print("Multiple session test completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())