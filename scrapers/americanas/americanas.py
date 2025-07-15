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
            pix = None
            old_price = None
            rating = None
            total_review = None
            link = None

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

            #Preço antigo
            old_price_tag = product.select_one('.ProductCard_discountPrice__Q2BeA')
            old_price_text = old_price_tag.text.strip()
            match = re.search(r"[\d\.,]+", old_price_text)
            if match:
                valor_str = match.group()
                old_price = float(valor_str.replace('.', '').replace(',', '.'))

            #Rating
            rating_tag = product.select_one('.avg-rating')
            if rating_tag:
                rating_text = rating_tag.text.strip()
                if rating_text:
                    rating = float(rating_text.replace(',', '.'))
            else:
                rating = None

            #total Reviews
            total_review_tag = product.select_one('.review-count')
            if total_review_tag:
                total_review_text = total_review_tag.text.strip()
                if total_review_text:
                    total_review = int(total_review_text.replace('(', '').replace(')', ''))
            else:
                total_review = None
            
            #Link do Produto
            link_tag = product.select_one('div.ProductGrid_vertical__TCnHK a')
            if link_tag:
                href = link_tag.get('href')
                if href:
                    link = 'https://www.americanas.com.br' + href

            if title:
                all_data.append({'title': title, 
                                 'price pix': pix,
                                 'old price' : old_price,
                                 'rating' : rating,
                                 'total review' : total_review,
                                 'product link' : link
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