import re
from urllib.parse import urlparse, urlunparse
import requests
from bs4 import BeautifulSoup

def build_ml_paginated_url(base_url, page, items_per_page=50):
    if page < 1:
        page = 1

    start_item = ((page - 1) * items_per_page) + 1

    parsed_url = urlparse(base_url)
    path = parsed_url.path

    path = re.sub(r'_Desde_\d+', '', path)
    path = re.sub(r'_NoIndex_True', '', path)

    if page == 1:
        path += "_NoIndex_True"
    else:
        path += f"_Desde_{start_item}_NoIndex_True"

    return urlunparse((parsed_url.scheme, parsed_url.netloc, path, '', '', ''))

def get_total_pages(base_url, items_per_page=50):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    total_text = soup.select_one('.ui-search-search-result__quantity-results')
    if total_text:
        match = re.search(r'([\d.]+)', total_text.text.replace('.', ''))
        if match:
            total_results = int(match.group(1))
            total_pages = (total_results + items_per_page - 1) // items_per_page
            return total_pages
    return 1

def generate_paginated_urls(base_url):
    items_per_page = 50
    total_pages = get_total_pages(base_url, items_per_page)
    urls = [build_ml_paginated_url(base_url, page, items_per_page) for page in range(1, total_pages + 1)]
    return urls