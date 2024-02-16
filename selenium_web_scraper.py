from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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
    
    with open("selenium_scraped_data.csv", "w", newline="") as csvfile:
     
        fields = ["product", "price", "img_link"]
  
        writer = csv.DictWriter(csvfile, fieldnames=fields, quoting=csv.QUOTE_ALL)
  
        writer.writeheader()
  
        writer.writerows(data)


def run(driver) -> None:
    
    driver.get('https://scrapeme.live/shop/')
    
    data = scrape_data(driver)
    
    print(data)
    
    save_as_csv(data)


def main() -> None:
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    
    run(driver)
    
    driver.quit()


if __name__ == "__main__":
    
    main()