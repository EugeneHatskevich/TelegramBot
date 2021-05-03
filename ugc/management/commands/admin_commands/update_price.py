from ugc.models import Product
from ugc.management.commands.parse import parse_data


def update_price(context):
    product_list = Product.objects.all()
    for product in product_list:
        result = parse_data(product.product_url, 'price')
        current_price = result['prices']['current']['amount']
        min_price = result['prices']['min']['amount']
        product.old_price = product.current_price
        product.current_price = current_price
        product.average_price = min_price
        product.save()
    print('Цены были обновлены')
