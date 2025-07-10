def get_description(products):

    all_data = []

    sponsored_texts = ['Sponsored', 'Patrocinado', 'Publicidade']
    ignored_titles = ['pesquisa', 'precisa', 'resultado', 'ajuda']

    for product in products:
        title_tag = product.select_one('h2.a-size-base-plus') or product.select_one('h2.a-size-medium') or product.select_one('h2')
        price_whole = product.select_one('span.a-price-whole')
        price_fraction = product.select_one('span.a-price-fraction')
        review = product.select_one('span.a-size-base.s-underline-text')
        stars_recived = product.select_one('span.a-icon-alt ')
        link_tag = product.select_one('a.a-link-normal.s-no-outline')

        title_text = title_tag.text.strip() if title_tag else 'N/A'
        price_text = (price_whole.text + price_fraction.text).strip() if price_whole and price_fraction else 'N/A'
        review_text = review.text.strip() if review else '0'
        stars_text = stars_recived.text.strip() if stars_recived else 'N/A'
        product_url = "https://www.amazon.com.br" + link_tag['href'] if link_tag else 'N/A'
        
        if any(word in title_text.lower() for word in ignored_titles):
            continue

        is_sponsored = False
        for tag in product.find_all(['span', 'div']):
            text = tag.get_text(strip=True).lower() 
            if any(keyword.lower() in text for keyword in sponsored_texts):
                is_sponsored = True
                break
            if tag.has_attr('aria-label') and any(keyword.lower() in tag['aria-label'].lower() for keyword in sponsored_texts):
                is_sponsored = True
                break

        item_data = {
            'title': title_text,
            'price': price_text,
            'number_of_reviews': review_text,
            'sponsored': is_sponsored,
            'stars_out_of_5': stars_text[:3],
            'product link' : product_url
        }

        all_data.append(item_data)

    return all_data
