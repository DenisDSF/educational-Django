import time

from django.test import TestCase

from .factories import CommentFactory, ArticleFactory
from ..models import Article
from ..services import get_news, get_article_comments


class GetNewsTest(TestCase):
    fixtures = ['Article', 'Author', 'ArticleTag']

    def test_get_news(self):
        """
        Case: Тест получения статей из фикстуры.
        Expected: Получены упорядоченные по дате статьи.
        Самая свежая статья с титулом 'Погода 1'.
        """
        self.articles = get_news()
        self.verifiable_article = self.articles[0]
        self.verifiable_title = 'Погода 1'
        self.assertEqual(self.verifiable_article.title, self.verifiable_title)


class GetArticleCommentsTest(TestCase):
    def setUp(self):
        ArticleFactory.create()
        self.article = Article.objects.all()[0]
        CommentFactory.create_batch(4, article=self.article)
        self.text = 'Test comments'
        CommentFactory.create(text=self.text, article=self.article)


    def test_get_article_comments(self):
        """
        Case: Тест получения комментариев с применением фабрики.
        Expected: Получены пять упорядоченных по дате комментариев. Самый
        новый комментарий с текстом self.text.
        """
        self.comments = get_article_comments(self.article.pk)
        self.verifiable_comment = self.comments[0]
        self.assertEqual(len(self.comments), 5)
        self.assertEqual(self.verifiable_comment.text, self.text)