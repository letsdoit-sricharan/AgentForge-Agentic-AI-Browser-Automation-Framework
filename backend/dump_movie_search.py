import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('https://in.bookmyshow.com/', wait_until='domcontentloaded')
        await page.wait_for_timeout(2000)
        
        # Close city modal or select Mumbai
        await page.click('li:has-text("Mumbai") >> visible=true')
        await page.wait_for_timeout(2000)
        
        # Click the search button
        await page.click('div[aria-label^="Search for Movies"]')
        await page.wait_for_timeout(2000)
        
        with open('bms_movie_search.html', 'w', encoding='utf-8') as f:
            f.write(await page.content())
        await page.screenshot(path='bms_movie_search.png')
        await browser.close()

asyncio.run(main())
