from django.test import TestCase
from django.test.client import Client


class ViewTest(TestCase):
    def test_index_page(self):
        self.client = Client()
        self.response = self.client.get('/index/')
        self.assertEqual(self.response.status_code, 200)