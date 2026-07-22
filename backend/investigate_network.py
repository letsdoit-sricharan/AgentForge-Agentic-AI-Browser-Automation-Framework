import asyncio
import json
import os
from playwright.async_api import async_playwright

async def run():
    out_dir = "network_logs"
    os.makedirs(out_dir, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        req_count = 0
        async def handle_response(response):
            nonlocal req_count
            req_type = response.request.resource_type
            url = response.url
            if req_type in ["fetch", "xhr"] and "in.bookmyshow.com" in url:
                try:
                    data = await response.json()
                    req_count += 1
                    with open(f"{out_dir}/req_{req_count}.json", "w", encoding="utf-8") as f:
                        json.dump({
                            "url": url,
                            "method": response.request.method,
                            "data": data
                        }, f, indent=2)
                except Exception as e:
                    pass

        page.on("response", handle_response)
        
        print("Navigating to BookMyShow...")
        await page.goto("https://in.bookmyshow.com/explore/home")
        
        print("Selecting city...")
        try:
            await page.locator('input[placeholder="Search for your city"]').fill("Mumbai")
            await page.locator('div[data-result-item="true"]:has-text("Mumbai")').first.click(timeout=5000)
        except Exception as e:
            print("City selection failed or skipped:", e)
            
        print("Clicking movie...")
        try:
            search_btn = page.locator('div[aria-label^="Search for Movies"]')
            await search_btn.click(timeout=5000)
            search_box = page.locator('#search input[type="text"]')
            await search_box.fill("Kalki")
            await page.locator("a[href*='/movies/']").first.click(timeout=5000)
        except Exception as e:
            print("Movie selection failed:", e)
        
        print("Clicking Book Tickets...")
        await page.locator("role=button[name='Book tickets'i]").first.click(timeout=10000, force=True)
        
        # In case there's a 2D/3D selection popup
        try:
            await page.locator("role=button[name='2D'i]").first.click(timeout=3000)
        except:
            pass
            
        print("Selecting showtime...")
        showtimes = page.locator("text=AM").locator("..").locator("..").locator("a")
        if await showtimes.count() > 0:
            await showtimes.first.click()
        else:
            showtimes = page.locator("text=PM").locator("..").locator("..").locator("a")
            await showtimes.first.click()
            
        print("Accepting terms...")
        try:
            await page.locator("text=Accept").first.click(timeout=3000)
        except:
            pass
            
        print("Selecting quantity...")
        try:
            await page.locator('li[id="quantity-1"]').click(timeout=3000)
            await page.locator("role=button[name='Select Seats'i]").click(timeout=3000)
        except:
            pass
            
        print("Waiting for canvas to load...")
        await page.locator("canvas").first.wait_for(timeout=10000)
        await asyncio.sleep(5)  # Wait for all network requests to finish
        
        print("Dumping window variables...")
        window_vars = await page.evaluate('''() => {
            const vars = [];
            for (let prop in window) {
                if (window.hasOwnProperty(prop)) {
                    vars.push(prop);
                }
            }
            return vars;
        }''')
        with open(f"{out_dir}/window_vars.json", "w", encoding="utf-8") as f:
            json.dump(window_vars, f, indent=2)
            
        await browser.close()
        print(f"Captured {req_count} JSON responses.")

if __name__ == "__main__":
    asyncio.run(run())
