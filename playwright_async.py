import asyncio
import time
from playwright.async_api import Playwright, async_playwright
from playwright.async_api import Page, expect
import csv

async def scrape_data(page):
    
    scraped_elements = []
 
    items = await page.query_selector_all("li.product")
 
    for i in items:
     
        scraped_element = {}

        el_title = await i.query_selector("h2")

        scraped_element["product"] = await el_title.inner_text()

        el_price = await i.query_selector("span.woocommerce-Price-amount")

        scraped_element["price"] = await el_price.text_content()

        image = await i.query_selector("a.woocommerce-LoopProduct-link.woocommerce-loop-product__link > img")

        scraped_element["img_link"] = await image.get_attribute("src")

        scraped_elements.append(scraped_element)
    
    return scraped_elements


async def save_as_csv(data):
    
	with open("async_scraped_data.csv", "w", newline="") as csvfile:
     
		fields = ["product", "price", "img_link"]
  
		writer = csv.DictWriter(csvfile, fieldnames=fields, quoting=csv.QUOTE_ALL)
  
		writer.writeheader()
  
		writer.writerows(data)


async def run(playwright: Playwright) -> None:
    
    browser = await playwright.chromium.launch(headless=False)
 
    context = await browser.new_context()

    page = await context.new_page()

    await page.goto("https://scrapeme.live/shop/", timeout=0)
    
    time.sleep(3)
    
    data = await scrape_data(page)

    print(data)
    
    await save_as_csv(data)

    await context.close()
    
    await browser.close()


async def main() -> None:
    
    async with async_playwright() as asyncplaywright:
        
        await run(asyncplaywright)


if __name__ == "__main__":
    
    asyncio.run(main())