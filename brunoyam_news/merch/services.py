from .models import Category, Product

def get_available_products(category_name):
    if Category.objects.filter(name=category_name).exists():
        available_products = Product.objects.select_related('category')\
            .filter(category__name=category_name)\
            .exclude(stock=0, supplies=False)
        return available_products
    else:
        return 'Not exist'