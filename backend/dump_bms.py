import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('https://in.bookmyshow.com/explore/home')
        await page.wait_for_timeout(5000)
        await page.screenshot(path='bms_loaded.png')
        with open('bms.html', 'w', encoding='utf-8') as f:
            f.write(await page.content())
        await browser.close()

asyncio.run(main())