from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import re

from utils.url_pagination_mercado_livre import generate_paginated_urls

def mercado_livre_scraper_product(driver, base_url):
    all_data = []
    wait = WebDriverWait(driver, 10)

    all_urls = generate_paginated_urls(base_url)

    for url in all_urls:
        try:
            driver.get(url)
            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.poly-component__title')
                )
            )
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            products = soup.select('.ui-search-result__wrapper')

            for product in products:

                #Titulo
                title_tag = product.select_one('.poly-component__title')
                title = title_tag.text.strip() if title_tag else None

                # Preço atual (Pix)
                price_tag = product.select_one('.poly-price__current .andes-money-amount__fraction')
                price = float(price_tag.text.strip().replace('.', '')) if price_tag else None

                #Old Price
                old_price_tag = product.select_one('.poly-component__price .andes-money-amount__fraction')
                old_price = float(old_price_tag.text.strip().replace('.', '')) if old_price_tag else None

                #Link
                link_tag = product.select_one('.poly-component__title-wrapper a')
                link = link_tag['href'] if link_tag else None

                #Avaliações
                review_tag = product.select_one('span.andes-visually-hidden')
                review = review_tag.text.strip() if review_tag else None

                rating = None
                total_review = None

                if review:
                    review = review.replace(',', '.')
                    match = re.search(r'Avaliação ([\d.]+) de 5\. \(([\d.,]+) avaliações\)', review)
                    if match:
                        rating = float(match.group(1))
                        total_review = int(match.group(2).replace('.', '').replace(',', ''))

                if title:
                    all_data.append({
                        'title' : title,
                        'price' : price,
                        'old price' : old_price,
                        'rating' : rating,
                        'total_review' : total_review,
                        'link' : link
                    })

        except Exception as e:
            print(f"Erro ao processar a URL: {url}")
            print(f"Detalhes do erro: {e}")
            continue 

    return all_data