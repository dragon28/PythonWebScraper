import time
from playwright.sync_api import Playwright, sync_playwright
from playwright.sync_api import Page, expect
import csv

def scrape_data(page):
    
    scraped_elements = []
 
    items = page.query_selector_all("li.product")
 
    for i in items:
     
        scraped_element = {}

        el_title = i.query_selector("h2")

        scraped_element["product"] = el_title.inner_text()

        el_price = i.query_selector("span.woocommerce-Price-amount")

        scraped_element["price"] = el_price.text_content()

        image = i.query_selector("a.woocommerce-LoopProduct-link.woocommerce-loop-product__link > img")

        scraped_element["img_link"] = image.get_attribute("src")

        scraped_elements.append(scraped_element)
    
    return scraped_elements


def save_as_csv(data):
    
	with open("sync_scraped_data.csv", "w", newline="") as csvfile:
     
		fields = ["product", "price", "img_link"]
  
		writer = csv.DictWriter(csvfile, fieldnames=fields, quoting=csv.QUOTE_ALL)
  
		writer.writeheader()
  
		writer.writerows(data)


def run(playwright: Playwright) -> None:
    
    browser = playwright.chromium.launch(headless=False)
 
    context = browser.new_context()

    page = context.new_page()

    page.goto("https://scrapeme.live/shop/", timeout=0)
    
    time.sleep(3)
    
    data = scrape_data(page)

    print(data)
    
    save_as_csv(data)

    context.close()
    
    browser.close()


def main():
    
    with sync_playwright() as syncplaywright:
        
        run(syncplaywright)
    

if __name__ == "__main__":
    
    main()