from django.shortcuts import render, get_object_or_404
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
    if not products:
        return HttpResponseNotFound()
    context = {
        'category_name': category_name,
        'products': products
    }
    return render(request, 'products/products_list.html', context)

def product(request, category_name, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product,
        'category_name': category_name
    }
    return render(request, 'products/product.html', context)