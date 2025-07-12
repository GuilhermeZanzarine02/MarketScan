from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import re

from utils.url_pagination import build_paginated_url
from const.const import human_delay

def magalu_scraper_product(driver, base_url):
    all_data = []
    page_count = 1
    max_pages = 7
    wait = WebDriverWait(driver, 10)

    while page_count <= max_pages:
        url = build_paginated_url(base_url, page_count)
        driver.get(url)
        human_delay()

        try:
            wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, 'h2[data-testid="product-title"]')
                )
            )

            print(f'[Página {page_count}] Produtos encontrados.')
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            titles = soup.select('h2[data-testid="product-title"]')
            regular_prices = soup.select('p[data-testid="installment"]')
            pix_prices = soup.select('p[data-testid="price-value"]')

            for title, regular_price, pix_price in zip(titles, regular_prices, pix_prices):
    
                regular_raw = regular_price.text.strip()
                match_regular = re.search(r'R\$[\s]?([\d\.,]+)', regular_raw)
                regular_numeric = float(match_regular.group(1).replace('.', '').replace(',', '.')) if match_regular else None

                pix_raw = pix_price.text.strip()
                match_pix = re.search(r'R\$[\s]?([\d\.,]+)', pix_raw)
                pix_numeric = float(match_pix.group(1).replace('.', '').replace(',', '.')) if match_pix else None

                item_data = {
                    'title': title.text.strip(),
                    'regular price': regular_numeric,
                    'pix price': pix_numeric
                }

                all_data.append(item_data)

            page_count += 1
        except Exception as e:
            print(f"Erro na página {page_count}: {e}")
            break

    return all_data