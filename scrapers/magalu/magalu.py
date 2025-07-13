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
            wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, '[data-testid="product-card-content"]')
            ))

            print(f'[Página {page_count}] Produtos encontrados.')
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            products = soup.select('[data-testid="product-card-content"]')

            for product in products:
                # Título
                title_tag = product.select_one('h2[data-testid="product-title"]')
                title = title_tag.text.strip() if title_tag else None

                # Preço regular
                regular_tag = product.select_one('p[data-testid="installment"]')
                if regular_tag:
                    match_regular = re.search(r'R\$[\s]?([\d\.,]+)', regular_tag.text)
                    regular_price = float(match_regular.group(1).replace('.', '').replace(',', '.')) if match_regular else None
                else:
                    regular_price = None

                # Preço Pix
                pix_tag = product.select_one('p[data-testid="price-value"]')
                if pix_tag:
                    match_pix = re.search(r'R\$[\s]?([\d\.,]+)', pix_tag.text)
                    pix_price = float(match_pix.group(1).replace('.', '').replace(',', '.')) if match_pix else None
                else:
                    pix_price = None
                
                #Link do Produto
                li_element = product.find_parent('li')
                link_tag = li_element.select_one('a[data-testid="product-card-container"]') if li_element else None
                link = (
                    'https://www.magazineluiza.com.br' + link_tag['href']
                    if link_tag and link_tag.has_attr('href') else None
                )

                # Somente se tiver título
                if title:
                    all_data.append({
                        'title': title,
                        'regular price': regular_price,
                        'pix price': pix_price,
                        'Product Link' : link
                    })

            page_count += 1

        except Exception as e:
            print(f"Erro na página {page_count}: {e}")
            break

    return all_data