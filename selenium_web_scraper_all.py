from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import csv


def scrape_data(driver):
    
    scraped_elements = []
 
    items = driver.find_elements(By.CSS_SELECTOR, 'li.product')
    
    for i in items:
     
        scraped_element = {}

        el_title = i.find_element(By.CSS_SELECTOR, 'h2')

        scraped_element["product"] = str(el_title.text)

        el_price = i.find_element(By.CSS_SELECTOR, 'span.woocommerce-Price-amount')

        scraped_element["price"] = str(el_price.text)

        image = i.find_element(By.CSS_SELECTOR, 'a.woocommerce-LoopProduct-link.woocommerce-loop-product__link > img')

        scraped_element["img_link"] = str(image.get_attribute("src"))

        scraped_elements.append(scraped_element)
    
    return scraped_elements


def save_as_csv(data):
    
    with open("selenium_scraped_data_all.csv", "w", newline="") as csvfile:
     
        fields = ["product", "price", "img_link"]
  
        writer = csv.DictWriter(csvfile, fieldnames=fields, quoting=csv.QUOTE_ALL)
  
        writer.writeheader()
  
        writer.writerows(data)


def get_current_page_number(driver):
    
    page_numbers = driver.find_elements(By.CSS_SELECTOR, "nav.woocommerce-pagination > ul.page-numbers > li > span.page-numbers.current")
    
    page_numbers = [i.text for i in page_numbers]
    
    current_page = page_numbers[0]
    
    print(current_page)
    
    return int(current_page)


def list_filter_numeric_values_only(item_list):
    
    return [int(i) for i in item_list if i.isdigit()]


def get_largest_number_list(item_list):
    
    return max(item_list)


def get_max_page_numbers(driver):
    
    page_numbers =  driver.find_elements(By.CSS_SELECTOR, "nav.woocommerce-pagination > ul.page-numbers > li")
    
    max_page_numbers =  [i.text for i in page_numbers]
    
    return get_largest_number_list(list_filter_numeric_values_only(max_page_numbers))


def get_next_page_link(driver):
    
    pagination = driver.find_elements(By.CSS_SELECTOR, "nav.woocommerce-pagination > ul.page-numbers > li > a.next.page-numbers")
    
    #page_numbers = pagination.find_elements(By.CSS_SELECTOR, "ul.page-numbers")
    
    #if page_numbers.find_elements(By.CSS_SELECTOR, "a.next.page-numbers"):
    if pagination:
        
        next_page = pagination[0].get_attribute('href')
    
    else:
        
        next_page = ""
    
    return str(next_page)


def run(driver) -> None:
    
    data = []
    
    driver.get('https://scrapeme.live/shop/')
    
    #data = scrape_data(driver)
    
    time.sleep(3)
    
    loop = True
    
    while(loop):
        
        time.sleep(3)
        
        data.extend(scrape_data(driver))

        if get_current_page_number(driver) < get_max_page_numbers(driver):
            
            next_page_link = get_next_page_link(driver)
        
        else:
            
            loop = False
            break
        
        if next_page_link is not None or next_page_link != "":
            
            driver.get(next_page_link)
            
        else:
            
            loop = False
            break
    
    
    print(data)
    
    save_as_csv(data)


def main() -> None:
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    
    run(driver)
    
    driver.quit()


if __name__ == "__main__":
    
    main()