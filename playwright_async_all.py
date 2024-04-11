import asyncio
import time
from playwright.async_api import Playwright, async_playwright
from playwright.async_api import Page, expect
import csv

async def scrape_data(page):
    
    scraped_elements = []
 
    items = await page.locator("li.product").all()
 
    for i in items:
     
        scraped_element = {}

        el_title = i.locator("h2")

        scraped_element["product"] = await el_title.inner_text()

        el_price = i.locator("span.woocommerce-Price-amount")

        scraped_element["price"] = await el_price.text_content()

        image = i.locator("a.woocommerce-LoopProduct-link.woocommerce-loop-product__link > img")

        scraped_element["img_link"] = await image.get_attribute("src")

        scraped_elements.append(scraped_element)
    
    return scraped_elements


async def save_as_csv(data):
    
    with open("playwright_async_scraped_data_all.csv", "w", newline="") as csvfile:
     
        fields = ["product", "price", "img_link"]
  
        writer = csv.DictWriter(csvfile, fieldnames=fields, quoting=csv.QUOTE_ALL)
  
        writer.writeheader()
  
        writer.writerows(data)


async def get_current_page_number(page):
    
    page_numbers = await page.locator("nav.woocommerce-pagination")
    
    page_numbers = await page_numbers.locator("ul.page-numbers")
    
    current_page = await page_numbers.locator("span.page-numbers.current").all_inner_texts()[0]
    
    return int(current_page)


async def list_filter_numeric_values_only(item_list):
    
    return [int(i) for i in item_list if i.isdigit()]


async def get_largest_number_list(item_list):
    
    return await max(item_list)


async def get_max_page_numbers(page):
    
    page_numbers = await page.locator("nav.woocommerce-pagination")
    
    page_numbers = await page_numbers.locator("ul.page-numbers")
    
    max_page_numbers = await page_numbers.locator("li").all_text_contents()
    
    return await get_largest_number_list(await list_filter_numeric_values_only(max_page_numbers))


async def get_next_page_link(page):
    
    pagination = await page.locator("nav.woocommerce-pagination")
    
    page_numbers = await pagination.locator("ul.page-numbers")
    
    if await page.query_selector("a.next.page-numbers") is not None:
        
        next_page = await page_numbers.locator("a.next.page-numbers").nth(0).get_attribute('href')
    
    else:
        
        next_page = ""
    
    return str(next_page)


async def run(playwright: Playwright) -> None:
    
    data = []
    
    browser = await playwright.chromium.launch(headless=False)
 
    context = await browser.new_context()

    page = await context.new_page()

    await page.goto("https://scrapeme.live/shop/", timeout=0)
    
    await asyncio.sleep(3)
    
    await page.wait_for_load_state("domcontentloaded")
    
    while(await get_current_page_number(page) <= await get_max_page_numbers(page)):
        
        await asyncio.sleep(3)
    
        await page.wait_for_load_state("domcontentloaded")
        
        await data.extend(scrape_data(page))

        if await get_current_page_number(page) < await get_max_page_numbers(page):
            
            next_page_link = await get_next_page_link(page)
        
        else:
            
            break
        
        if next_page_link is not None or next_page_link != "":
            
            await page.goto(next_page_link, timeout=0)
            
        else:
            
            break
    
    print(data)
    
    await save_as_csv(data)

    await context.close()
    
    await browser.close()


async def main() -> None:
    
    async with async_playwright() as asyncplaywright:
        
        await run(asyncplaywright)


if __name__ == "__main__":
    
    asyncio.run(main())