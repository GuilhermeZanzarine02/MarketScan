from datetime import datetime
import pandas as pd
import numpy as np
from pathlib import Path
import re

def clean_price(price_str):
    
    cleaned = re.sub(r'[^\d,\.]', '', price_str)

    if ',' in cleaned and cleaned.count(',') == 1 and cleaned.count('.') <= 1:
        cleaned = cleaned.replace(',', '.')

    if cleaned.count('.') > 1:
        parts = cleaned.split('.')
        cleaned = ''.join(parts[:-1]) + '.' + parts[-1]

    return cleaned

def handle_data(all_data, file_type,  price_order):

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    downloads_path = str(Path.home() / "Downloads")

    raw_data = all_data

    data = pd.DataFrame(raw_data)

    data['price'] = data['price'].apply(clean_price).replace('', np.nan)
    data['price'] = pd.to_numeric(data['price'], errors='coerce').fillna(0)

    data['number_of_reviews'] = pd.to_numeric(data['number_of_reviews'], errors='coerce').fillna(0).astype(int)

    data['stars_out_of_5'] = data['stars_out_of_5'].astype(str).str.replace(',', '.').replace('', np.nan)
    data['stars_out_of_5'] = pd.to_numeric(data['stars_out_of_5'], errors='coerce').fillna(0)

    file = file_type.lower()
    order_file =  price_order.lower()

    path = None 

    try:
        if file == 'excel(.xlsx)' and order_file == 'highest to lowest':
            data = data.sort_values(by='price', ascending=False)
            path = f"{downloads_path}/data_scraped_highest_to_lowest_price_{timestamp}.xlsx"
            data.to_excel(path, index=False)

        elif file == 'excel(.xlsx)' and order_file == 'lowest to highest':
            data = data.sort_values(by='price', ascending=True)
            path = f"{downloads_path}/data_scraped_lowest_to_highest_price_{timestamp}.xlsx"
            data.to_excel(path, index=False)

        elif file == 'csv(.csv)' and order_file == 'highest to lowest':
            data = data.sort_values(by='price', ascending=False)
            path = f"{downloads_path}/data_scraped_highest_to_lowest_price_{timestamp}.csv"
            data.to_csv(path, index=False)

        elif file == 'csv(.csv)' and order_file == 'lowest to highest':
            data = data.sort_values(by='price', ascending=True)
            path = f"{downloads_path}/data_scraped_lowest_to_highest_price_{timestamp}.csv"
            data.to_csv(path, index=False)

        if path is not None:
            print(f"Arquivo salvo com sucesso em: {path}")
        else:
            print("Nenhum arquivo salvo — verifique parâmetros.")
            
    except Exception as e:
        print(f'Erro ao salvar o arquivo: {e}')