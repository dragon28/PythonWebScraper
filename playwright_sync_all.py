import time
from playwright.sync_api import Playwright, sync_playwright
from playwright.sync_api import Page, expect
import csv

def scrape_data(page):
    
    scraped_elements = []
 
    items = page.locator("li.product").all()
 
    for i in items:
     
        scraped_element = {}

        el_title = i.locator("h2")

        scraped_element["product"] = el_title.inner_text()

        el_price = i.locator("span.woocommerce-Price-amount")

        scraped_element["price"] = el_price.text_content()

        image = i.locator("a.woocommerce-LoopProduct-link.woocommerce-loop-product__link > img")

        scraped_element["img_link"] = image.get_attribute("src")

        scraped_elements.append(scraped_element)
    
    return scraped_elements


def save_as_csv(data):
    
    with open("playwright_sync_scraped_data_all.csv", "w", newline="") as csvfile:
     
        fields = ["product", "price", "img_link"]
  
        writer = csv.DictWriter(csvfile, fieldnames=fields, quoting=csv.QUOTE_ALL)
  
        writer.writeheader()
  
        writer.writerows(data)


def get_current_page_number(page):
    
    page_numbers = page.locator("nav.woocommerce-pagination")
    
    page_numbers = page_numbers.locator("ul.page-numbers")
    
    current_page = page_numbers.locator("span.page-numbers.current").all_inner_texts()[0]
    
    return int(current_page)


def list_filter_numeric_values_only(item_list):
    
    return [int(i) for i in item_list if i.isdigit()]


def get_largest_number_list(item_list):
    
    return max(item_list)


def get_max_page_numbers(page):
    
    page_numbers = page.locator("nav.woocommerce-pagination")
    
    page_numbers = page_numbers.locator("ul.page-numbers")
    
    max_page_numbers = page_numbers.locator("li").all_text_contents()
    
    return get_largest_number_list(list_filter_numeric_values_only(max_page_numbers))


def get_next_page_link(page):
    
    pagination = page.locator("nav.woocommerce-pagination")
    
    page_numbers = pagination.locator("ul.page-numbers")
    
    if page.query_selector("a.next.page-numbers") is not None:
        
        next_page = page_numbers.locator("a.next.page-numbers").nth(0).get_attribute('href')
    
    else:
        
        next_page = ""
    
    return str(next_page)


def run(playwright: Playwright) -> None:
    
    data = []
    
    browser = playwright.chromium.launch(headless=False)
 
    context = browser.new_context()

    page = context.new_page()

    page.goto("https://scrapeme.live/shop/", timeout=0)
    
    time.sleep(3)
    
    page.wait_for_load_state("domcontentloaded")
    
    loop = True
    
    while(loop):
        
        time.sleep(3)
    
        page.wait_for_load_state("domcontentloaded")
        
        data.extend(scrape_data(page))

        if get_current_page_number(page) < get_max_page_numbers(page):
            
            next_page_link = get_next_page_link(page)
        
        else:
            
            loop = False
            break
        
        if next_page_link is not None or next_page_link != "":
            
            page.goto(next_page_link, timeout=0)
            
        else:
            
            loop = False
            break

    print(data)
    
    save_as_csv(data)

    context.close()
    
    browser.close()


def main():
    
    with sync_playwright() as syncplaywright:
        
        run(syncplaywright)
    

if __name__ == "__main__":
    
    main()