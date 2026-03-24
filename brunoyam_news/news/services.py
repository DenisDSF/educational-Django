from .models import Article, Comment


def get_news():
    return (Article.objects.filter(status=Article.Status.PUBLISH).
            order_by('-pub_date'))

def get_article_comments(article_id):
    return (Comment.objects.filter(article_id=article_id).
            order_by('-created_at'))