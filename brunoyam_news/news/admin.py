from django.contrib import admin
from .models import Article, ArticleTag, Author

admin.site.register(Article)
admin.site.register(ArticleTag)
admin.site.register(Author)