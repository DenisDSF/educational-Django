from datetime import datetime, timezone
from django.test import TestCase
from .models import Author, ArticleTag, Article


class AuthorModelTest(TestCase):
    fixtures = ['Author']

    def test_author_creation(self):
        """
        Case: Тест создания объектов модели Author из фикстуры.
        Expected: Созданы три объекта модели Author.
        Объект модели pk=1 имеет имя 'Иван Петров'.
        """
        self.name_to_verify = 'Иван Петров'
        self.authors = Author.objects.all()
        self.verifiable_author = Author.objects.get(pk=1)
        self.authors_count = len(self.authors)
        self.assertEqual(self.authors_count, 3)
        self.assertEqual(self.verifiable_author.name, self.name_to_verify)


class ArticleTagTest(TestCase):
    fixtures = ['ArticleTag']

    def test_article_tag_creation(self):
        """
        Case: Тест создания объектов модели ArticleTag из фикстуры.
        Expected: Созданы пять объектов модели ArticleTag.
        Объект модели pk=2 имеет имя 'Наука'.
        """
        self.tag_to_verify = 'Наука'
        self.article_tags = ArticleTag.objects.all()
        self.verifiable_article_tag = ArticleTag.objects.get(pk=2)
        self.article_tags_count = len(self.article_tags)
        self.assertEqual(self.article_tags_count, 5)
        self.assertEqual(self.verifiable_article_tag.name, self.tag_to_verify)


class ArticleTest(TestCase):
    fixtures = ['Author', 'ArticleTag', 'Article']

    def test_article_creation(self):
        """
        Case: Тест создания объектов модели Article из фикстуры.
        Expected: Созданы 8 объектов модели Article.
        Объект модели pk=5 имеет автора из модели Author с именем
        'Иван Петров', титул 'Научно-техническая новость 1', описание
        'Описание научно-технической новости 1', текст 'Текст
        научно-технической новости 1'. Дата и время публикации объекта модели -
        '2026-01-01 07:00:00'. Статус объекта модели 'PUBLISH'.
        Первый тег объекта 'Наука', второй 'Техника' из модели ArticleTag.
        Изображение со ссылкой 'images/nt1.jpg'.
        """
        self.author_name_to_verify = 'Иван Петров'
        self.title_to_verify = 'Научно-техническая новость 1'
        self.description_to_verify = 'Описание научно-технической новости 1'
        self.text_to_verify = 'Текст научно-технической новости 1'
        self.pub_date_to_verify = datetime(2026, 1, 1, 7, 0,
                                           tzinfo=timezone.utc)
        self.status_to_verify = Article.Status.PUBLISH
        self.first_tag_to_verify = 'Наука'
        self.second_tag_to_verify = 'Техника'
        self.image_path_to_verify = 'images/nt1.jpg'

        self.articles = Article.objects.all()
        self.verifiable_article = Article.objects.get(pk=5)
        self.articles_count = len(self.articles)
        self.assertEqual(self.articles_count, 8)
        self.assertEqual(
            self.verifiable_article.author.name,
            self.author_name_to_verify
        )
        self.assertEqual(
            self.verifiable_article.title,
            self.title_to_verify
        )
        self.assertEqual(
            self.verifiable_article.description,
            self.description_to_verify
        )
        self.assertEqual(
            self.verifiable_article.text,
            self.text_to_verify
        )
        self.assertEqual(
            self.verifiable_article.pub_date,
            self.pub_date_to_verify
        )
        self.assertEqual(
            self.verifiable_article.status,
            self.status_to_verify
        )
        self.assertEqual(
            self.verifiable_article.article_tags.all()[0].name,
            self.first_tag_to_verify
        )
        self.assertEqual(
            self.verifiable_article.article_tags.all()[1].name,
            self.second_tag_to_verify
        )
        self.assertEqual(
            self.verifiable_article.image,
            self.image_path_to_verify
        )

    def test_models_related_fields(self):
        """
        Case: Тест связанных полей Atricle с ArticleTag,
        а так же Article с Author.
        Expected: Статья объекта sefl.author совпадает с проверяемым объектом
        модели Article. Статья найденная по тегам self.tag1 и self.tag2
        совпадают с проверяемым объектом модели Article.
        """
        self.author = Author.objects.get(pk=1)
        self.tag1 = ArticleTag.objects.get(pk=2)
        self.tag2 = ArticleTag.objects.get(pk=3)
        self.verifiable_article = Article.objects.get(pk=5)
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
        self.author = Author.objects.get(pk=1)
        self.tag1 = ArticleTag.objects.get(pk=2)
        self.tag2 = ArticleTag.objects.get(pk=3)
        self.author.delete()
        self.tag1.delete()
        self.tag2.delete()
        self.verifiable_article = Article.objects.get(pk=5)
        self.assertEqual(self.verifiable_article.author, None)
        self.assertEqual(len(self.verifiable_article.article_tags.all()), 0)