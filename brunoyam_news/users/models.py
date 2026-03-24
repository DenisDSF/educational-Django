from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(
        'Имя',
        max_length=64,
        null=True,
        blank=True
    )
    surname = models.CharField(
        'Фамилия',
        max_length=64,
        null=True,
        blank=True
    )
    email = models.EmailField(
        'Почта',
        max_length=128,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username