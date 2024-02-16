import asyncio
from playwright.async_api import async_playwright

async def task_playwright():
    
    async with async_playwright() as async_playwright:
        
        browser = await async_playwright.chromium.launch()
        
        page = await browser.new_page()
        
        await page.goto("https://scrapeme.live/shop/")
        
        print(await page.title())
        
        await browser.close()


async def main():
    
    await task_playwright()
    
if __name__ == "__main__":
    
    asyncio.run(main())