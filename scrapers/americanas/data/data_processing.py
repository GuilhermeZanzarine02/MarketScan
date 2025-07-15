from datetime import datetime
import pandas as pd
from pathlib import Path


def americanas_handle_data(all_data, file_type, price_order, rows):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    downloads_path = str(Path.home() / "Downloads")
    data = pd.DataFrame(all_data)
    file = file_type.lower()
    order_file =  price_order.lower()
    path = None 

    try:
        if file == 'excel(.xlsx)' and order_file == 'highest to lowest':
            if rows:
                rows = int(rows)
                data = data.sort_values(by='price', ascending=False).head(rows)
                path = f"{downloads_path}/data_scraped_highest_to_lowest_price_{timestamp}.xlsx"
                data.to_excel(path, index=False)
            else:
                data = data.sort_values(by='price', ascending=False)
                path = f"{downloads_path}/data_scraped_highest_to_lowest_price_{timestamp}.xlsx"
                data.to_excel(path, index=False)

        elif file == 'excel(.xlsx)' and order_file == 'lowest to highest':
            if rows:
                rows = int(rows)
                data = data.sort_values(by='price', ascending=True).head(rows)
                path = f"{downloads_path}/data_scraped_lowest_to_highest_price_{timestamp}.xlsx"
                data.to_excel(path, index=False)
            else:
                data = data.sort_values(by='price', ascending=True)
                path = f"{downloads_path}/data_scraped_highest_to_lowest_price_{timestamp}.xlsx"
                data.to_excel(path, index=False)
        
        elif file == 'excel(.xlsx)' and order_file == 'raw':
            if rows:
                rows = int(rows)
                path = f"{downloads_path}/data_scraped_lowest_to_highest_price_{timestamp}.xlsx"
                data = data.head(rows)
                data.to_excel(path, index=False)
            else:
                path = f"{downloads_path}/data_scraped_highest_to_lowest_price_{timestamp}.xlsx"
                data.to_excel(path, index=False)

        elif file == 'csv(.csv)' and order_file == 'highest to lowest':
            if rows:
                rows = int(rows)
                data = data.sort_values(by='price', ascending=False).head(rows)
                path = f"{downloads_path}/data_scraped_highest_to_lowest_price_{timestamp}.csv"
                data.to_csv(path, index=False)
            else:
                data = data.sort_values(by='price', ascending=False)
                path = f"{downloads_path}/data_scraped_highest_to_lowest_price_{timestamp}.csv"
                data.to_csv(path, index=False)

        elif file == 'csv(.csv)' and order_file == 'lowest to highest':
            if rows:
                rows = int(rows)
                data = data.sort_values(by='price', ascending=True).head(rows)
                path = f"{downloads_path}/data_scraped_lowest_to_highest_price_{timestamp}.csv"
                data.to_csv(path, index=False)
            else:
                data = data.sort_values(by='price', ascending=True)
                path = f"{downloads_path}/data_scraped_lowest_to_highest_price_{timestamp}.csv"
                data.to_csv(path, index=False)
        
        elif file == 'csv(.csv)' and order_file == 'raw':
            if rows:
                rows = int(rows)
                path = f"{downloads_path}/data_scraped_lowest_to_highest_price_{timestamp}.csv"
                data = data.head(rows)
                data.to_csv(path, index=False)
            else:
                path = f"{downloads_path}/data_scraped_highest_to_lowest_price_{timestamp}.csv"
                data.to_csv(path, index=False)

        if path is not None:
            print(f"Arquivo salvo com sucesso em: {path}")
        else:
            print("Nenhum arquivo salvo — verifique parâmetros.")
            
    except Exception as e:
        print(f'Erro ao salvar o arquivo: {e}')