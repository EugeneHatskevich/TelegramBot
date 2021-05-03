import requests
import json


def parse_data(url: str, content: str = 'data'):
    product_id = url.split("/")[-1]
    if content == 'data':
        product_data = requests.get(f'https://catalog.onliner.by/sdapi/catalog.api/products/{product_id}').content
        result = json.loads(product_data)
    elif content == 'price':
        price_data = requests.get(
            f'https://catalog.onliner.by/sdapi/catalog.api/products/{product_id}/prices-history?period=6m').content
        result = json.loads(price_data)
    return result
