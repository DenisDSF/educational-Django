from .models import Product

def get_available_products(category_name):
    available_products = Product.objects.select_related('category')\
        .filter(category__name=category_name)\
        .exclude(stock=0, supplies=False)
    return available_products