import asyncio
import logging
from app.browser_engine.managers.browser_manager import BrowserManager
from app.browser_engine.models.browser_options import BrowserOptions

logging.basicConfig(level=logging.INFO)

async def main():
    options = BrowserOptions(headless=False)
    browser_manager = BrowserManager(options)
    await browser_manager.start()
    session_manager = await browser_manager.create_session()
    page = await session_manager.new_page()
    session = session_manager._session
    
    # Use playwright internal page for ease of debugging
    pw_page = page._page
    
    await pw_page.goto("https://in.bookmyshow.com/")
    await pw_page.wait_for_timeout(2000)
    
    # Click Mumbai
    await pw_page.click('li:has-text("Mumbai") >> visible=true')
    await pw_page.wait_for_timeout(2000)
    
    # Click Search
    await pw_page.click('div[aria-label^="Search for Movies"]')
    await pw_page.wait_for_timeout(2000)
    
    # Type Alpha
    await pw_page.fill('#search input[type="text"]', 'Alpha')
    await pw_page.wait_for_timeout(2000)
    
    # Click Alpha
    await pw_page.click('text=Alpha')
    await pw_page.wait_for_timeout(3000)
    
    # Click Book tickets
    await pw_page.click('button:has-text("Book tickets")')
    await pw_page.wait_for_timeout(3000)
    
    with open('bms_debug_alpha_book.html', 'w', encoding='utf-8') as f:
        f.write(await pw_page.content())
    await pw_page.screenshot(path='bms_debug_alpha_book.png')
    
    # Do not close, wait 1 sec
    await pw_page.wait_for_timeout(1000)

asyncio.run(main())
