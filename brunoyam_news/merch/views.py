from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from .models import Category, Product
from .services import get_available_products

def merch_category(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'category/merch_category.html', context)

def products_list(request, category_name):
    products = get_available_products(category_name)
    if products != 'Not exist':
        context = {
            'category_name': category_name,
            'products': products
        }
        return render(request, 'products/products_list.html', context)
    else:
        return HttpResponseNotFound()

def product(request, category_name, product_id):
    try:
        product = Product.objects.get(id=product_id)
        context = {
            'product': product,
            'category_name': category_name
        }
        return render(request, 'products/product.html', context)
    except Product.DoesNotExist:
        return HttpResponseNotFound()