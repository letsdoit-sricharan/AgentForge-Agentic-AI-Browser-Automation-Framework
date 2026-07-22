import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('https://in.bookmyshow.com/', wait_until='domcontentloaded')
        await page.wait_for_timeout(2000)
        await page.fill('input[placeholder="Search for your city"]', 'Mumbai')
        await page.wait_for_timeout(2000)
        with open('bms_search.html', 'w', encoding='utf-8') as f:
            f.write(await page.content())
        await page.screenshot(path='bms_search.png')
        await browser.close()

asyncio.run(main())
