from flask import Flask, render_template, request

from const.const import get_driver

from scrapers.amazon.data.data_processing import amazon_handle_data
from scrapers.amazon.amazon import amz_scraper_product_title

from scrapers.magalu.magalu import magalu_scraper_product
from scrapers.magalu.data.data_processing import magalu_handle_data

from scrapers.mercado_livre.mercado_livre import mercado_livre_scraper_product
from scrapers.mercado_livre.data.data_processing import mercado_livre_handle_data

from scrapers.americanas.americanas import americanas_scraper_product
from scrapers.americanas.data.data_processing import americanas_handle_data

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
                amazon_handle_data(all_data, file_type, price_order, rows)
                message = 'Arquivo gerado com sucesso!'

            elif store == 'magalu':
                all_data = magalu_scraper_product(driver, base_url)
                magalu_handle_data(all_data, file_type, price_order, rows)
                message = 'Arquivo gerado com sucesso!'

            elif store == 'mercado_livre':
                all_data = mercado_livre_scraper_product(driver, base_url)
                mercado_livre_handle_data(all_data, file_type, price_order, rows)
                message = 'Arquivo gerado com sucesso!'

            elif store == 'americanas':
                all_data = americanas_scraper_product(driver, base_url)
                americanas_handle_data(all_data, file_type, price_order, rows)
                message = 'Arquivo gerado com sucesso!'

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