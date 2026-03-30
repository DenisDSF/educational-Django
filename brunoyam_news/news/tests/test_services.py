from django.test import TestCase

from .factories import CommentFactory, ArticleFactory
from ..models import Article
from ..services import (get_news, get_raw_article_comments_text_and_username,
                        get_article_comments_with_anon_users)
from users.models import User


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
        CommentFactory.create_batch(3, article=self.article)
        self.text = 'Test comments'
        self.username = 'TestUser1'
        self.password = 'GFGHssdsHGFGHYY443JJGBSDvvvv'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
        )
        CommentFactory.create(
            article=self.article,
            user=self.user,
            is_anon=False
        )
        CommentFactory.create(
            article=self.article,
            user=self.user,
            is_anon=True,
            text=self.text
        )

    def test_get_article_comments(self):
        """
        Case: Тест получения комментариев с применением фабрики.
        Expected: Получены пять упорядоченных по дате комментариев. Самый
        новый комментарий с текстом self.text. Первый по свежести комментарий
        анонимен. Второй по свежести комментарий не анонимен.
        """
        self.raw_comments = get_raw_article_comments_text_and_username(
            self.article.pk
        )
        self.comments = get_article_comments_with_anon_users(
            self.raw_comments
        )
        self.first_verifiable_comment = self.comments[0]
        self.second_verifiable_comment = self.comments[1]
        self.assertEqual(len(self.comments), 5)
        self.assertEqual(self.first_verifiable_comment['text'], self.text)
        self.assertIsNone(self.first_verifiable_comment['user__username'])
        self.assertEqual(
            self.second_verifiable_comment['user__username'],
            self.username
        )