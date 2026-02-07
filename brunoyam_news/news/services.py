from .models import Article


def get_news():
    return Article.objects.filter(status=Article.Status.PUBLISH).order_by('-pub_date')