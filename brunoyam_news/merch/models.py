from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=100
    )
    image = models.CharField(
        max_length=100,
        null=True
    )


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(
        max_length=100,
        null=True
    )
    stock = models.IntegerField(default=0)
    supplies = models.BooleanField(default=True)
    product_description = models.TextField(
        default='The description and specifications '
                'are temporarily unavailable.'
    )