from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

from utils.url_pagination import build_paginated_url
from scrapers.amazon.product_scraper import get_description

def amz_scraper_product_title(driver, base_url):

    all_data  = []
    page_count  =  1
    wait = WebDriverWait(driver, 10)

    while True:
        url = build_paginated_url(base_url, page_count)
        driver.get(url)

        try:
            wait.until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, 'h2.a-size-base-plus.a-spacing-none.a-color-base.a-text-normal')
                )
            )
        except:
            print("No titles found on the page, end of pagination.")
            break

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        products = soup.select('div.s-result-item')

        page_data = get_description(products)
        
        for product in page_data:

            new_product = {}

            for key, value in product.items():
                new_product[key] = value
            
            all_data.append(new_product)

        next_button = driver.find_elements(By.CSS_SELECTOR, "a.s-pagination-next")
        if not next_button or not next_button[0].is_enabled():
           print('Last page reached')
           break
        
        page_count += 1

    return all_data