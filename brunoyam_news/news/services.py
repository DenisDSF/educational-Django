from .models import Article, Comment


def get_news():
    return (Article.objects.filter(status=Article.Status.PUBLISH).
            order_by('-pub_date'))

def get_raw_article_comments_text_and_username(article_id):
    return (Comment.objects.filter(article_id=article_id).
            values('user__username', 'is_anon', 'text').
            order_by('-created_at'))

def get_article_comments_with_anon_users(comments_list):
    for i in comments_list:
        if i['user__username'] and i['is_anon']:
            i['user__username'] = None
    return comments_list