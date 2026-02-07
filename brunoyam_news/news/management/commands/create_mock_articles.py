from django.core.management.base import BaseCommand

from news.factories import ArticleFactory
from news.models import Article


class Command(BaseCommand):
    help = "Create sample data in database"

    def handle(self, *args, **options):
        for i in range(5):
            ArticleFactory.create(status=Article.Status.PUBLISH)
