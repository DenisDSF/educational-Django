from datetime import timezone, datetime
import factory
from factory.django import DjangoModelFactory
from .models import Author, ArticleTag, Article


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.Faker('name')


class ArticleTagFactory(DjangoModelFactory):
    class Meta:
        model = ArticleTag

    name = factory.Faker('word')


class ArticleFactory(DjangoModelFactory):
    class Meta:
        model = Article

    author = factory.SubFactory(AuthorFactory)
    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('sentence', nb_words=5)
    text = factory.Faker('text', max_nb_chars=300)
    status = Article.Status.DRAFT
    pub_date = factory.Faker(
        'date_time_ad',
        tzinfo=timezone.utc,
        start_datetime=datetime(2025, 1, 1)
    )
    image = factory.Faker('file_name', extension='jpg')

    @factory.post_generation
    def article_tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.article_tags.add(tag)
        else:
            tags = ArticleTagFactory.create_batch(2)
            self.article_tags.set(tags)