from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
import re

from const.const import human_delay 

def americanas_scraper_product(driver, base_url, max_clicks=10):
    all_data = []
    driver.get(base_url)

    clicks = 0

    while clicks < max_clicks:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        products = soup.select('.ProductCard_productCard__MwY4X')

        for product in products:
            #Titulo
            title_tag = product.select_one('.ProductCard_productName__mwx7Y')
            title = title_tag.text.strip() if title_tag else None

            #Preço Pix
            pix_price_tag = product.select_one('.ProductCard_productPrice__XFEqu')
            pix_price = pix_price_tag.text.strip()
            match = re.search(r"[\d\.,]+", pix_price)
            if match:
                valor_str = match.group()
                pix = float(valor_str.replace('.', '').replace(',', '.'))

            if title:
                all_data.append({'title': title, 
                                 'price pix': pix
                                 })
        try:
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'button[data-testid="pagination-button"]')
                )
            )
            load_more_button.click()
            human_delay()
            clicks += 1

            WebDriverWait(driver, 10).until(
                lambda d: len(BeautifulSoup(d.page_source, 'html.parser')
                              .select('.ProductGrid_vertical__TCnHK')) 
            )

        except TimeoutException:
            print("Botão 'Mostrar mais produtos' não encontrado ou fim dos produtos.")
            break

    print(f"Coletados {len(all_data)} produtos em {clicks} cliques.")
    return all_data
