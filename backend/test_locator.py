import asyncio
from playwright.async_api import async_playwright

async def test():
    p = await async_playwright().start()
    browser = await p.chromium.launch()
    page = await browser.new_page()
    with open("bms_test_failure.html", "r", encoding="utf-8") as f:
        await page.set_content(f.read())
    
    count_loc = page.locator('li[id="quantity-1"]')
    try:
        await count_loc.click(timeout=2000)
        print("quantity-1 clicked!")
    except Exception as e:
        print("quantity-1 click error:", str(e))
        
    btn_loc = page.locator("role=button[name='Select Seats'i]")
    try:
        await btn_loc.click(timeout=2000)
        print("Select Seats clicked!")
    except Exception as e:
        print("Select Seats click error:", str(e))

    await browser.close()
    p.stop()

if __name__ == "__main__":
    asyncio.run(test())
