from django.test import TestCase
from django.test.client import Client

from .factories import CommentFactory, ArticleFactory
from..models import Article


class IndexViewTest(TestCase):
    fixtures = ['Author', 'ArticleTag', 'Article']

    def test_index_status_code(self):
        """
        Case: Тест получения статус-кода страницы index.
        Expected: Страница со статус-кодом 200.
        """
        self.client = Client()
        self.response = self.client.get('/index/')
        self.assertEqual(self.response.status_code, 200)

    def test_index_uses_correct_template(self):
        """
        Case: Тест используемых шаблонов страницы.
        Expected: Страницы с используемыми шаблонами index.html и base.html.
        """
        self.client = Client()
        self.response = self.client.get('/index/')
        self.assertTemplateUsed(self.response, 'index.html')
        self.assertTemplateUsed(self.response, 'base.html')

    def test_index_content(self):
        """
        Case: Тест получения контента из фикстуры.
        Expected: Фикстура с 6 опубликованными новостями, 1 неактивной
        новостью и 1 новостью на модерации. Одна из новостей с титулом
        'Научно-техническая новость 2'.
        """
        self.client = Client()
        self.response = self.client.get('/index/')
        self.assertEqual(len(self.response.context['all_news']), 6)
        self.assertContains(self.response, 'Научно-техническая новость 2')
        self.assertNotContains(self.response, 'На модерации')


class ArticleDetailViewTest(TestCase):
    fixtures = ['Author', 'ArticleTag', 'Article']

    def setUp(self):
        self.article = Article.objects.all()[0]
        CommentFactory.create_batch(14, article=self.article)
        self.text = 'Test comments'
        CommentFactory.create(text=self.text, article=self.article)
        self.test_article = Article.objects.all()[0]
        self.url = f'/articles/{self.test_article.pk}/'

    def test_article_status_code(self):
        """
        Case: Тест получения статус-кода страницы 'articles/<int:pk>/'.
        Expected: Страница со статус-кодом 200.
        """
        self.client = Client()
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)

    def test_article_uses_correct_template(self):
        """
        Case: Тест используемых шаблонов страницы.
        Expected: Страницы с используемыми шаблонами article.html и base.html.
        """
        self.client = Client()
        self.response = self.client.get(self.url)
        self.assertTemplateUsed(self.response, 'article.html')
        self.assertTemplateUsed(self.response, 'base.html')

    def test_article_content(self):
        """
        Case: Тест получения контента из фикстуры.
        Expected: Первая новость c титулом 'Научно-техническая новость 2'.
        У первой новости 15 комментариев.
        На странице отображены 10 комментариев, последний с текстом
        self.text.
        """
        self.client = Client()
        self.response = self.client.get(self.url)
        self.assertContains(self.response, 'Научно-техническая новость 2')
        self.assertEqual(len(self.response.context['comments']), 10)
        self.assertEqual(self.response.context['is_paginated'], True)
        self.assertEqual(self.response.context['comments'][0].text, self.text)


class CreateCommentViewTest(TestCase):
    def setUp(self):
        ArticleFactory.create()
        self.test_article = Article.objects.all()[0]
        self.url = f'/articles/{self.test_article.pk}/add_comment'

    def test_create_comment_view(self):
        """
        Case: Тест создания двух комментариев на странице
        'articles/<int:pk>/'.
        Expected: Созданы два комментария c текстом self.first_comment_text и
        self.last_comment_text.
        """
        self.client = Client()
        self.first_comment_text ='test comment 1'
        self.last_comment_text = 'test comment 2'
        self.response = self.client.post(
            self.url,
            {'text': self.first_comment_text}
        )
        self.assertEqual(self.response.status_code, 302)
        self.response = self.client.post(
            self.url,
            {'text': self.last_comment_text},
            follow=True
        )
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(
            self.response.context['comments'][0].text,
            self.last_comment_text)
        self.assertEqual(
            self.response.context['comments'][1].text,
            self.first_comment_text)