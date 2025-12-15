from email.policy import default

from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField()

    def __str__(self):
        return self.title

class Article(models.Model):
    """
    Статья на сайте.
    """
    class Status(models.TextChoices):
        DRAFT = 'draft', 'На модерации'
        PUBLISH = 'publish', 'Готово к публикации'
        INACTIVE = 'inactive', 'Неактивная'

    author = models.ForeignKey('users.User', related_name='articles', on_delete=models.SET_NULL, null=True, default=None)

    title = models.CharField('Заголовок новости', max_length=64, unique=True)
    description = models.CharField('Описание новости', max_length=200)
    text = models.TextField('Текст новости')
    status = models.CharField(max_length=8, choices=Status.choices, default=Status.DRAFT)


    pub_date = models.DateTimeField('Дата публикации новости')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


