from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def build_paginated_url(base_url, page):

    url_parts = list(urlparse(base_url))
    query = parse_qs(url_parts[4])

    query.pop('page', None)

    if page > 1:
        query['page'] = [str(page)]

        url_parts[4] = urlencode(query, doseq=True)
    
    return urlunparse(url_parts)
