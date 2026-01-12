from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from .models import Category, Product

def merch_category(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'category/merch_category.html', context)

def checking_product_availability(all_products):
    available_products = all_products.exclude(stock=0, supplies=False)
    return available_products

def products_list(request, category_name):
    if Category.objects.filter(name=category_name).exists():
        all_products = Product.objects.select_related('category')\
            .filter(category__name=category_name)
        available_products = checking_product_availability(all_products)
        context = {
            'category_name': category_name,
            'products': available_products
        }
        return render(request, 'products/products_list.html', context)
    else:
        return HttpResponseNotFound()

def product(request, category_name, product_id):
    category_name = category_name
    try:
        product = Product.objects.get(id=product_id)
        context = {
            'product': product,
            'category_name': category_name
        }
        return render(request, 'products/product.html', context)
    except Product.DoesNotExist:
        return HttpResponseNotFound()