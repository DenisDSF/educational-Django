from django.utils import timezone
from django.test import TestCase
from .models import Author, ArticleTag, Article


class AuthorModelTest(TestCase):
    def setUp(self):
        self.name = 'Test name'
        self.author = Author.objects.create(name=self.name)

    def test_author_creation(self):
        """
        Case: Тест создания объекта модели Author.
        Expected: Создан объект модели Author с именем self.name.
        """
        self.assertEqual(self.author.name, self.name)


class ArticleTagTest(TestCase):
    def setUp(self):
        self.name = 'Tag name'
        self.article_tag = ArticleTag.objects.create(name=self.name)

    def test_article_tag_creation(self):
        """
        Case: Тест создания объекта модели ArticleTag.
        Expected: Создан новый объект модели ArticleTag с именем self.name.
        """
        self.assertEqual(self.article_tag.name, self.name)


class ArticleTest(TestCase):
    def setUp(self):
        self.author_name = 'Автор статьи'
        self.author = Author.objects.create(name=self.author_name)

        self.title = 'Титул статьи'
        self.description = 'Описание статьи'
        self.text = 'Текст статьи'
        self.now = timezone.now()

        self.article = Article.objects.create(
            author=self.author,
            title=self.title,
            description=self.description,
            text=self.text,
            status=Article.Status.PUBLISH,
            pub_date=self.now,
            image=None
        )

        self.tag1_name = 'Первый тег'
        self.tag1 = ArticleTag.objects.create(name=self.tag1_name)
        self.tag2_name = 'Второй тег'
        self.tag2 = ArticleTag.objects.create(name=self.tag2_name)
        self.article.article_tags.add(self.tag1, self.tag2)

    def test_article_creation(self):
        """
        Case: Тест создания нового объекта модели Article.
        Expected: Создан объект модели Article с автором с
        именем self.author_name из модели Author,
        с титулом self.title, описанием self.description,
        текстом self.text, датой и временем публикации равной дату и времени
        начала теста, статусом PUBLISH, а так же двумя тегами self.tag1 и
        self.tag2 из модели ArticleTag.
        """
        self.assertEqual(self.article.author.name, self.author_name)
        self.assertEqual(self.article.title, self.title)
        self.assertEqual(self.article.description, self.description)
        self.assertEqual(self.article.text, self.text)
        self.assertEqual(self.article.pub_date, self.now)
        self.assertEqual(self.article.status, Article.Status.PUBLISH)
        self.assertEqual(
            self.article.article_tags.all()[0].name,
            self.tag1_name
        )
        self.assertEqual(
            self.article.article_tags.all()[1].name,
            self.tag2_name
        )
        self.assertEqual(
            self.article.image,
            None
        )

    def test_models_related_fields(self):
        """
        Case: Тест связанных полей Atricle с ArticleTag,
        а так же Article с Author.
        Expected: Статья объекта sefl.author совпадает с созданным объектом
        модели Article. Статьи найденные по тегам self.tag1 и self.tag2
        совпадают с созданным объектом модели Article.
        """
        self.assertEqual(self.author.articles.all()[0], self.article)
        self.assertEqual(self.tag1.articles.all()[0], self.article)
        self.assertEqual(self.tag2.articles.all()[0], self.article)

    def test_models_integration(self):
        """
        Case: Тест взаимодействия между моделями Atricle и ArticleTag,
        а так же Article и Author.
        Expected: Удаление объекта self.author устанавливает аргумент author у
        объекта self.article равным None. Удаление тегов self.tag1 и self.tag2
        так же удаляет эти теги у объекта self.article.
        """
        self.author.delete()
        self.tag1.delete()
        self.tag2.delete()
        self.article = Article.objects.all()[0]
        self.assertEqual(self.article.author, None)
        self.assertEqual(len(self.article.article_tags.all()), 0)
