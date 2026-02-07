from django.test import TestCase

from .factories import AuthorFactory, ArticleTagFactory, ArticleFactory
from .models import Author, ArticleTag, Article


class AuthorModelTest(TestCase):
    def setUp(self):
        AuthorFactory.create_batch(4)
        self.name = 'Test name'
        AuthorFactory.create(name=self.name)

    def test_author_creation(self):
        """
        Case: Тест создания пяти объектов модели Author.
        Expected: Созданы пять объектов модели Author.
        Пятый объект создан с именем 'self.name'.
        """
        self.authors = Author.objects.all()
        self.verifiable_author = self.authors[4]
        self.authors_count = len(self.authors)
        self.assertEqual(self.authors_count, 5)
        self.assertEqual(self.verifiable_author.name, self.name)


class ArticleTagTest(TestCase):
    def setUp(self):
        ArticleTagFactory.create_batch(2)
        self.name = 'Tag name'
        ArticleTagFactory.create(name=self.name)
        ArticleTagFactory.create_batch(2)

    def test_article_tag_creation(self):
        """
        Case: Тест создания пяти объектов модели ArticleTag.
        Expected: Созданы пять объектов модели ArticleTag.
        Третья с именем 'self.name'.
        """
        self.article_tags = ArticleTag.objects.all()
        self.verifiable_article_tags = self.article_tags[2]
        self.article_tags_count = len(self.article_tags)
        self.assertEqual(self.article_tags_count, 5)
        self.assertEqual(self.verifiable_article_tags.name, self.name)


class ArticleTest(TestCase):
    def setUp(self):
        ArticleFactory.create_batch(4)
        self.image_name = 'photo1.jpg'
        ArticleFactory.create(status=Article.Status.PUBLISH, image=self.image_name)

    def test_article_creation(self):
        """
        Case: Тест создания пяти объектов модели Article.
        Expected: Созданы пять объектов модели Article.
        Пятый объект со статусом 'PUBLISH'.
        """
        self.articles = Article.objects.all()
        self.verifiable_article = self.articles[4]
        self.articles_count = len(self.articles)
        self.assertEqual(self.articles_count, 5)
        self.assertEqual(self.verifiable_article.status, Article.Status.PUBLISH)
        self.assertEqual(
            self.verifiable_article.image,
            self.image_name
        )

    def test_models_related_fields(self):
        """
        Case: Тест связанных полей Atricle с ArticleTag,
        а так же Article с Author.
        Expected: Статья объекта sefl.author совпадает с проверяемым объектом
        модели Article. Статья найденная по тегам self.tag1 и self.tag2
        совпадает с проверяемым объектом модели Article.
        """
        self.author = Author.objects.all()[0]
        self.tag1 = ArticleTag.objects.all()[0]
        self.tag2 = ArticleTag.objects.all()[1]
        self.verifiable_article = Article.objects.all()[0]
        self.assertEqual(self.author.articles.all()[0], self.verifiable_article)
        self.assertEqual(self.tag1.articles.all()[0], self.verifiable_article)
        self.assertEqual(self.tag2.articles.all()[0], self.verifiable_article)

    def test_models_integration(self):
        """
        Case: Тест взаимодействия между моделями Atricle и ArticleTag,
        а так же Article и Author.
        Expected: Удаление объекта self.author устанавливает аргумент author у
        объекта self.verifiable_article равным None.
        Удаление тегов self.tag1 и self.tag2 так же удаляет эти теги у
        объекта self.verifiable_article.
        """
        self.author = Author.objects.all()[0]
        self.tag1 = ArticleTag.objects.all()[0]
        self.tag2 = ArticleTag.objects.all()[1]
        self.verifiable_article = Article.objects.all()[0]
        self.article_title = self.verifiable_article.title
        self.author.delete()
        self.tag1.delete()
        self.tag2.delete()
        self.verifiable_article = Article.objects.get(
            title=self.article_title
        )
        self.assertEqual(self.verifiable_article.author, None)
        self.assertEqual(len(self.verifiable_article.article_tags.all()), 0)