from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ArticleTag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    Статья на сайте.
    """
    class Status(models.TextChoices):
        DRAFT = 'draft', 'На модерации'
        PUBLISH = 'publish', 'Готово к публикации'
        INACTIVE = 'inactive', 'Неактивная'

    author = models.ForeignKey(
        Author,
        related_name='articles',
        on_delete=models.SET_NULL,
        null=True,
    )

    title = models.CharField('Заголовок новости', max_length=64, unique=True)
    description = models.CharField('Описание новости', max_length=200)
    text = models.TextField('Текст новости')
    article_tags = models.ManyToManyField(
        ArticleTag,
        related_name='articles'
    )
    image = models.ImageField(
        upload_to='images/',
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=8,
        choices=Status.choices,
        default=Status.DRAFT)


    pub_date = models.DateTimeField('Дата публикации новости')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        related_name='comments',
        on_delete=models.CASCADE
    )
    text = models.TextField('Текст комментария')
    user = models.ForeignKey(
        'users.User',
        related_name='comments',
        on_delete=models.SET_NULL,
        null=True
    )
    is_anon = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def username(self):
        return self.user.username if self.user is not None else \
            'Анонимный пользователь'