from django.shortcuts import render
from .models import Category, Product

def merch_category(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'category/merch_category.html', context)

def products_list(request, category_name):
    category = Category.objects.get(name=category_name)
    products = category.products.exclude(stock=0, supplies=False)
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'products/products_list.html', context)

def product(request, category_name, product_id):
    category_name = category_name
    product = Product.objects.get(id=product_id)
    context = {
        'product': product,
        'category_name': category_name
    }
    return render(request, 'products/product.html', context)