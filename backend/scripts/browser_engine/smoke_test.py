"""
Smoke Test
==========

Purpose:
    Verify that the Playwright implementation layer works correctly.

This script verifies:

    PlaywrightAdapter
        ↓
    PlaywrightBrowser
        ↓
    PlaywrightSession
        ↓
    PlaywrightPage

Expected Flow:

    Launch Browser
        ↓
    Open Google
        ↓
    Print Title
        ↓
    Take Screenshot
        ↓
    Close Everything
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from app.browser_engine.implementations.playwright.playwright_adapter import (
    PlaywrightAdapter,
)
from app.browser_engine.implementations.playwright.playwright_browser import (
    PlaywrightBrowser,
)
from app.browser_engine.models.browser_options import BrowserOptions
from app.browser_engine.models.navigation_options import NavigationOptions
from app.browser_engine.models.screenshot_options import ScreenshotOptions


async def main() -> None:
    print("=" * 60)
    print("AgentForge Browser Engine Smoke Test")
    print("=" * 60)

    adapter = PlaywrightAdapter()
    browser = PlaywrightBrowser(adapter)

    print("Launching browser...")

    await browser.launch(
        BrowserOptions(
            headless=False,
        )
    )

    print("Browser launched.")

    session = await browser.new_session()

    print("Session created.")

    page = await session.new_page()

    print("Page created.")

    print("Opening Google...")

    await page.goto(
        "https://www.google.com",
        NavigationOptions(),
    )

    print("Google opened.")

    title = await page.title()

    print(f"Title: {title}")

    screenshot_path = Path("google_homepage.png")

    await page.screenshot(
        ScreenshotOptions(
            path=screenshot_path,
            full_page=True,
        )
    )

    print(f"Screenshot saved to: {screenshot_path.resolve()}")

    await page.close()

    print("Page closed.")

    await session.close()

    print("Session closed.")

    await browser.close()

    print("Browser closed.")

    print("\nSmoke test completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())