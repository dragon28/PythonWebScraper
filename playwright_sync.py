import time
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page, expect

def task_playwright():
    
    with sync_playwright() as sync_playwright:
        
        browser = sync_playwright.chromium.launch()
        
        page = browser.new_page()
        
        page.goto("https://scrapeme.live/shop/", timeout=0)
        
        time.sleep(3)
        
        print(page.title())
        
        browser.close()


def main():
    
    task_playwright()
    

if __name__ == "__main__":
    main()