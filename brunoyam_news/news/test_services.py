from django.test import TestCase

from .services import get_news


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


