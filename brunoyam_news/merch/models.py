from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):

    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        null=False)

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)