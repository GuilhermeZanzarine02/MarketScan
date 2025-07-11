from flask import Flask, render_template, request

from const.const import get_driver
from scrapers.amazon.amazon import amz_scraper_product_title
from data.data_processing import handle_data

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        driver = get_driver()
        base_url = request.form.get('url')
        price_order = request.form.get('sort')
        file_type = request.form.get('filetype')
        store = request.form.get('store').lower()
        rows = request.form.get('limit')

        if not base_url or not store:
            return render_template('index.html', message='Por favor, preencha a URL e escolha a loja.')

        try:
            if store == 'amazon':
                all_data = amz_scraper_product_title(driver, base_url)
                handle_data(all_data, file_type, price_order, rows)
                message = 'Arquivo gerado com sucesso!'
            elif store == 'magalu':
                message = 'Scraper da Magalu ainda em construção.'
            elif store == 'americanas':
                message = 'Scraper da Americanas ainda em construção.'
            else:
                message = 'Loja não suportada.'
        except Exception as e:
            message = f'Ocorreu um erro: {e}'
        finally:
            driver.quit()

        return render_template('index.html', message=message)

    return render_template('index.html')
    
if __name__ == '__main__':
    app.run(debug=True)