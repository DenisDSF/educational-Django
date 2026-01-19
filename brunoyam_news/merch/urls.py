from django.urls import path
from .views import merch_category, products_list, product


urlpatterns = [
    path('merch_category/', merch_category, name='merch_category'),
    path('merch_category/<str:category_name>/', products_list, name='products_list'),
    path('merch_category/<str:category_name>/<int:product_id>/', product, name='product')
]

